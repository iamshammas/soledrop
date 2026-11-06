from django.conf import settings
from django.shortcuts import get_object_or_404, render,redirect
# from .models import Coupon
from accounts.models import Address
from accounts.services import PaymentGatewayNotConfigured
from cart.models import Cart,CartItem
from .models import Order,OrderItem
from django.http import HttpResponse
from django.db import transaction
from .services.order_service import (
    create_order,
    create_order_after_payment,
    notify_online_payment_issue,
    start_online_payment,
)
from .services.razorpay import verify_razorpay_payment
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

# Create your views here.

RAZORPAY_CHECKOUT_SESSION_KEY = 'razorpay_checkout'

def apply_coupon(request):
    return HttpResponse("Coupon applied successfully!")



#another function to checkout | Order creation working properly
def checkouttt(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        full_name = first_name + ' ' +last_name
        address_line1 = request.POST.get('address_line1')
        address_line2 = request.POST.get('address_line2')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pin_code = request.POST.get('pin_code')
        country = request.POST.get('country')
        payment_method = request.POST.get('payment_method')
        cart_items = CartItem.objects.filter(cart__user=request.user)
        with transaction.atomic():
            order = Order.objects.create(
            user=request.user,
            name=full_name,
            email=email,
            phone=phone,
            address_line1=address_line1,
            address_line2=address_line2,
            city=city,
            state=state,
            pincode=pin_code,
            country=country,
            payment_method=payment_method
            )
            if order:
                order.total_amount = 0
                for item in cart_items:
                    order_item = OrderItem.objects.create(
                        order=order,
                        variant=item.variant,
                        quantity=item.quantity,
                        price_at_purchase=item.variant.product.new_price
                    )
                    order_item.save()
                    order.total_amount+= order_item.total_price
                    order.save()
                cart=Cart.objects.get(user=request.user)
                # cart.delete()
                cart.cart_items.all().delete()
                return redirect('orders:order_confirmation',order_id=order.id)
            else:
                print("Order creation failed")
                return redirect('orders:checkout')
    cart_subtotal = Cart.objects.filter(user=request.user).first().total_price
    cart_total = cart_subtotal if cart_subtotal >= 4999 else cart_subtotal+199
    addresses = Address.objects.filter(user=request.user)
    context = {
        'cart_subtotal' : cart_subtotal,
        'cart_total' : cart_total,
        'addresses' : addresses
    }
    return render(request, 'checkout.html',context)

@login_required
def checkout(request):
    if request.method == 'POST':
        # cart = get_object_or_404(Cart, user=request.user)
        cart, created = Cart.objects.get_or_create(user=request.user)
        address_id = request.POST.get('address_id')
        if address_id:
            address = Address.objects.get(id=address_id)
        else:
            address = Address(
                full_name=request.POST.get("full_name"),
                phone_number=request.POST.get("phone"),
                address=request.POST.get("address"),
                city=request.POST.get("city"),
                state=request.POST.get("state"),
                pin_code=request.POST.get("pin_code"),
                country=request.POST.get("country"),
            )
        payment_method = request.POST.get('payment_method')

        if payment_method == Order.PaymentMethod.ONLINE:
            try:
                payment_data = start_online_payment(address, cart)
            except PaymentGatewayNotConfigured:
                messages.error(
                    request,
                    'Online payment is not configured yet. Please choose cash on delivery.',
                )
                return redirect('orders:checkout')
            except (ValidationError, ValueError) as e:
                messages.error(request, str(e))
                return redirect('orders:checkout')

            request.session[RAZORPAY_CHECKOUT_SESSION_KEY] = payment_data
            return redirect('orders:order_payment')

        try:
            order = create_order(request.user,address,payment_method,cart)
            request.session.pop(RAZORPAY_CHECKOUT_SESSION_KEY, None)
            messages.success(request, "Order placed successfully.")
            return redirect('orders:order_confirmation',order_id=order.id)
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('orders:checkout')
    
    else:
        # cart = Cart.objects.get(user=request.user)
        cart, _ = Cart.objects.get_or_create(user=request.user)

        if not cart.items.exists():
            messages.error(request, "Your cart is empty.")
            return redirect('cart:cart_detail')
        addresses = Address.objects.filter(user=request.user)
        context = {
            'cart_subtotal' : cart.subtotal,
            'cart_total' : cart.total,
            'addresses' : addresses,
            'razorpay_configured': bool(
                settings.RAZORPAY_KEY_ID and settings.RAZORPAY_KEY_SECRET
            ),
        }
        return render(request, 'checkout.html',context)

@login_required
def order_payment(request):
    payment_data = request.session.get(RAZORPAY_CHECKOUT_SESSION_KEY) or {}

    if (
        not payment_data.get('razorpay_order_id')
        or not payment_data.get('amount_in_paise')
        or not settings.RAZORPAY_KEY_ID
        or not settings.RAZORPAY_KEY_SECRET
    ):
        messages.error(
            request,
            'Your payment session has expired. Please return to checkout.',
        )
        return redirect('orders:checkout')

    context = {
        'amount': payment_data.get('total_amount', ''),
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'razorpay_order_id': payment_data['razorpay_order_id'],
        'amount_in_paise': payment_data['amount_in_paise'],
    }
    return render(request, 'order_payment.html', context)


@login_required
@require_POST
def order_payment_verify(request):
    payment_data = request.session.get(RAZORPAY_CHECKOUT_SESSION_KEY) or {}
    expected_order_id = payment_data.get('razorpay_order_id')

    if not expected_order_id:
        messages.error(
            request,
            'Your payment session has expired. Please return to checkout.',
        )
        return redirect('orders:checkout')

    try:
        verified = verify_razorpay_payment(
            expected_order_id,
            request.POST.get('razorpay_order_id'),
            request.POST.get('razorpay_payment_id'),
            request.POST.get('razorpay_signature'),
        )
    except PaymentGatewayNotConfigured:
        messages.error(
            request,
            'Online payment is not configured yet. Please contact support.',
        )
        return redirect('orders:checkout')

    if not verified:
        messages.error(
            request,
            'Payment could not be verified. Please try again or contact support.',
        )
        return redirect('orders:order_payment')

    try:
        order = create_order_after_payment(request.user, payment_data)
    except ValidationError as e:
        notify_online_payment_issue(
            payment_data,
            request.POST.get('razorpay_payment_id'),
            str(e),
        )
        request.session.pop(RAZORPAY_CHECKOUT_SESSION_KEY, None)
        messages.error(
            request,
            'Payment was received, but the order could not be created. '
            'Please contact support with your payment reference.',
        )
        return redirect('cart:cart_detail')

    request.session.pop(RAZORPAY_CHECKOUT_SESSION_KEY, None)
    messages.success(request, 'Payment successful. Your order is confirmed.')
    return redirect('orders:order_confirmation', order_id=order.id)

@login_required
def order_confirmation(request,order_id):
    order = get_object_or_404(Order,id=order_id)
    context = {
        'order': order
    }
    return render(request,'order_confirmation.html',context)

@login_required
def order_list(request):
    qs = Order.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(qs, 5)  # 5 orders per page
    page_obj  = paginator.get_page(request.GET.get('page', 1))
    return render(request, 'order_list.html', {
        'orders': page_obj,
        'active_tab': 'orders',
    })

def order_detail(request,order_id):
    order = get_object_or_404(Order,id=order_id)
    context = {
        'order': order,
        'active_tab': 'orders',
    }
    return render(request, 'order_detail.html', context)

# def order_history(request):
    # Fetch the user's order history from the database
    # For example, you might want to retrieve Order objects associated with the user
    # orders = Order.objects.filter(user=request.user)

    # return render(request, 'order_list.html', {'orders': orders})