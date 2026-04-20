from django.conf import settings
from cart.models import Cart

def cart_data(request):
    cart = Cart.objects.filter(user=request.user.id).first() if request.user.is_authenticated else None
    if cart:
        cart_count = cart.items.count()
        cart_items = cart.items.all()
        cart_total = cart.total_price
        # cart_subtotal = Cart.objects.filter(user=request.user).first().total_price if cart_items else 0
    else:
        cart_count = 0
        cart_items = []
        cart_total = 0
    return {
        'cart_count': cart_count,
        'cart_items':cart_items,
        'cart_total': cart_total,
        # 'cart_subtotal':cart_subtotal
    }