from django.core.signals import request_finished
from django.shortcuts import get_object_or_404, render,redirect
# from .models import Coupon
from cart.models import Cart,CartItem
from .models import Order,OrderItem
from django.http import HttpResponse
from django.db import transaction

# Create your views here.

def apply_coupon(request):
    return HttpResponse("Coupon applied successfully!")

# def checkout(request):
#     if request.method == 'POST':
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         full_name = first_name + ' ' +last_name
#         address_line1 = request.POST.get('address_line1')
#         address_line2 = request.POST.get('address_line2')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#         city = request.POST.get('city')
#         state = request.POST.get('state')
#         pin_code = request.POST.get('pin_code')
#         country = request.POST.get('country')
#         payment_method = request.POST.get('payment_method')
#         cart_items = CartItem.objects.filter(cart__user=request.user) 
#         # price_at_purchase = cart_total
#         # print(cart_total)
#         # print(payment_method)
#         # Process the order placement logic here
#         order = Order.objects.create(
#             user=request.user,
#             name=full_name,
#             email=email,
#             phone=phone,
#             address_line1=address_line1,
#             address_line2=address_line2,
#             city=city,
#             state=state,
#             pin_code=pin_code,
#             country=country,
#             payment_method=payment_method
#         )
#         if order:
#             order.save()
#             total = 0
#             for item in cart_items:
#                 OrderItem.objects.create(
#                     order=order,
#                     variant=item.variant,
#                     quantity=item.quantity,
#                     price_at_purchase=item.variant.product.new_price,
#                 )
#                 total+=item.variant.product.new_price
#                 item.cart.items.remove(item)
#         # For example, you might want to create an Order object, save it to the database, etc.
        
#         # After processing the order, you can redirect to a confirmation page or render a success message
#         return render(request, 'order_confirmation.html', {'message': 'Order placed successfully!'})
#     else:
#         # If it's a GET request, simply render the checkout page
#         cart = Cart.objects.filter(user=request.user).first()
#         cart_items = cart.items.all() if cart else []
#         cart_count = cart.items.count() if cart else 0
#         cart_total = cart.total_price if cart else 0
#         j = 0
#         # j1 means no stock, j0 means it is available
#         for i in cart_items:
#             if not i.in_stock:
#                 j = 1
#         print('Stock available' if j==0 else 'Stock Not available')
#         context = {
#             'cart_items': cart_items,
#             'cart_count': cart_count,
#             'cart_total': cart_total,
#         }
#         return render(request, 'checkout.html', context)


#another function to checkout | Order creation working properly
def checkout(request):
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
        # for item in cart_items:
        #     print(item)
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
                cart.delete()
                return redirect('orders:order_confirmation',order_id=order.id)
            else:
                print("Order creation failed")
                return redirect('orders:checkout')

    return render(request, 'checkout.html')


def order_confirmation(request,order_id):
    order = get_object_or_404(Order,id=order_id)
    context = {
        'order': order
    }
    return render(request,'order_confirmation.html',context)

def order_list(request):
    orders=Order.objects.filter(user=request.user)
    return render(request,'order_list.html',{'orders':orders})

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