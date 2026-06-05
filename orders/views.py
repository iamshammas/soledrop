from django.shortcuts import get_object_or_404, render,redirect
# from .models import Coupon
from accounts.models import Address
from cart.models import Cart,CartItem
from .models import Order,OrderItem
from django.http import HttpResponse
from django.db import transaction
from .services.order_service import create_order
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.

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
        try:
            order = create_order(request.user,address,payment_method,cart)
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
            'addresses' : addresses
        }
        return render(request, 'checkout.html',context)

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
    return render(request,'order_list.html',{'orders':page_obj})

def order_detail(request,order_id):
    order = get_object_or_404(Order,id=order_id)
    context = {
        'order': order
    }
    return render(request,'order_detail.html',context)

# def order_history(request):
    # Fetch the user's order history from the database
    # For example, you might want to retrieve Order objects associated with the user
    # orders = Order.objects.filter(user=request.user)

    # return render(request, 'order_list.html', {'orders': orders})