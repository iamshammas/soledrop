from django.shortcuts import render
# from .models import Coupon
from cart.models import Cart
from django.http import HttpResponse

# Create your views here.

def apply_coupon(request):
    return HttpResponse("Coupon applied successfully!")

def checkout(request):
    if request.method == 'POST':
        # Process the order placement logic here
        # For example, you might want to create an Order object, save it to the database, etc.
        
        # After processing the order, you can redirect to a confirmation page or render a success message
        return render(request, 'order_confirmation.html', {'message': 'Order placed successfully!'})

    # If it's a GET request, simply render the checkout page
    cart = Cart.objects.filter(user=request.user).first()
    cart_items = cart.items.all() if cart else []
    cart_count = cart.items.count() if cart else 0
    cart_subtotal = cart.total_price if cart else 0
    context = {
        'cart_items': cart_items,
        'cart_count': cart_count,
        'cart_subtotal': cart_subtotal,
    }
    return render(request, 'checkout.html', context)


# def order_history(request):
    # Fetch the user's order history from the database
    # For example, you might want to retrieve Order objects associated with the user
    # orders = Order.objects.filter(user=request.user)

    # return render(request, 'order_list.html', {'orders': orders})