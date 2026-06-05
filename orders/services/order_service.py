from django.db import transaction
from django.core.exceptions import ValidationError
from orders.models import Order, OrderItem

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
            return order
    return 'payment is by RAZORPAY'

