import uuid
from decimal import Decimal

from django.db import transaction
from django.core.exceptions import ValidationError
from orders.models import Order, OrderItem
from cart.models import Cart, CartItem
from products.models import Variant
from .razorpay import create_razorpay_order
from .telegram import send_order_notification, send_telegram_message

def create_order(user, address, payment_method,cart):
    if payment_method == 'COD':
        with transaction.atomic():
            # STOCK VALIDATION
            for item in cart.items.select_related('variant').all():
                if item.quantity > item.variant.stock:
                    raise ValidationError(
                        f"{item.variant.product.name} has only "
                        f"{item.variant.stock} units available."
                    )
                
            # ORDER CREATION
            order = Order.objects.create(
                user=user,
                name=address.full_name,
                phone=address.phone_number,
                address=address.address,
                city=address.city,
                state=address.state,    
                pincode=address.pin_code,
                country=address.country,
                payment_method=payment_method,
                subtotal = cart.subtotal,
                shipping_charge = cart.shipping_charge,
                total_amount=cart.total
            )

            # CREATE ORDER_ITEMS & REDUCE STOCK
            for item in cart.items.select_related('variant','variant__product'):
                OrderItem.objects.create(
                    order=order,
                    variant=item.variant,
                    quantity=item.quantity,
                    price_at_purchase=item.variant.product.new_price
                )

                item.variant.stock -= item.quantity
                item.variant.save(update_fields=['stock'])

            # CART CLEARING
            cart.items.all().delete()
            try:
                send_order_notification(order)
            except Exception:
                pass
            return order
    return 'payment is by RAZORPAY'


def start_online_payment(address, cart):
    if not cart.items.exists():
        raise ValidationError('Your cart is empty.')

    items = []
    for item in cart.items.select_related('variant', 'variant__product').all():
        if item.quantity > item.variant.stock:
            raise ValidationError(
                f"{item.variant.product.name} has only "
                f"{item.variant.stock} units available."
            )

        items.append({
            'variant_id': item.variant_id,
            'quantity': item.quantity,
            'price': str(item.variant.product.new_price),
        })

    subtotal = cart.subtotal
    shipping_charge = cart.shipping_charge
    total_amount = subtotal + shipping_charge

    provider_order_id = create_razorpay_order(
        total_amount,
        f'cart-{cart.pk}-{uuid.uuid4().hex[:12]}',
    )

    return {
        'razorpay_order_id': provider_order_id,
        'items': items,
        'address': {
            'name': address.full_name,
            'phone': address.phone_number,
            'address': address.address,
            'city': address.city,
            'state': address.state,
            'pincode': address.pin_code,
            'country': address.country,
        },
        'subtotal': str(subtotal),
        'shipping_charge': str(shipping_charge),
        'total_amount': str(total_amount),
        'amount_in_paise': int((total_amount * 100).to_integral_value()),
    }


def create_order_after_payment(user, payment_data):
    items = payment_data.get('items') or []
    address = payment_data.get('address') or {}

    if not items:
        raise ValidationError('No items were found for this payment.')

    variant_ids = [item['variant_id'] for item in items]

    with transaction.atomic():
        variants = {
            variant.pk: variant
            for variant in Variant.objects.select_for_update()
            .filter(pk__in=variant_ids)
            .order_by('pk')
        }

        for item in items:
            variant = variants.get(item['variant_id'])

            if variant is None:
                raise ValidationError(
                    'One or more items in this order are no longer available.'
                )

            if item['quantity'] > variant.stock:
                raise ValidationError(
                    f"{variant.product.name} has only "
                    f"{variant.stock} units available."
                )

        order = Order.objects.create(
            user=user,
            name=address.get('name') or '',
            phone=address.get('phone') or '',
            address=address.get('address') or '',
            city=address.get('city') or '',
            state=address.get('state') or '',
            pincode=address.get('pincode') or '',
            country=address.get('country') or '',
            payment_method=Order.PaymentMethod.ONLINE,
            status=Order.Status.CONFIRMED,
            subtotal=Decimal(payment_data['subtotal']),
            shipping_charge=Decimal(payment_data['shipping_charge']),
            total_amount=Decimal(payment_data['total_amount']),
        )

        for item in items:
            variant = variants[item['variant_id']]
            quantity = item['quantity']

            OrderItem.objects.create(
                order=order,
                variant=variant,
                quantity=quantity,
                price_at_purchase=Decimal(item['price']),
            )

            variant.stock -= quantity
            variant.save(update_fields=['stock'])

        cart = Cart.objects.filter(user=user).first()

        if cart:
            for item in items:
                cart_item = CartItem.objects.filter(
                    cart=cart,
                    variant_id=item['variant_id'],
                ).first()

                if cart_item is None:
                    continue

                if cart_item.quantity <= item['quantity']:
                    cart_item.delete()
                else:
                    cart_item.quantity -= item['quantity']
                    cart_item.save(update_fields=['quantity'])

    try:
        send_order_notification(order)
    except Exception:
        pass

    return order


def notify_online_payment_issue(payment_data, payment_id, reason):
    message = (
        '⚠️ Online payment received but no order was created\n\n'
        f"Payment ID: {payment_id or 'unknown'}\n"
        f"Amount: ₹{payment_data.get('total_amount', '')}\n"
        f"Items: {sum(item['quantity'] for item in payment_data.get('items', []))}\n"
        f"Reason: {reason}"
    )

    try:
        send_telegram_message(message)
    except Exception:
        pass

