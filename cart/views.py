from itertools import product

from django.shortcuts import redirect, render

from products.models import Product
from cart.models import Cart, CartItem

# Create your views here.

def cart_detail(request):
    cart_items = Cart.objects.filter(user=request.user).first().items.all()
    cart_count = cart_items.count()
    cart_subtotal = Cart.objects.filter(user=request.user).first().total_price if cart_items else 0
    context = {
        'cart_items': cart_items,
        'cart_count': cart_count,
        'cart_subtotal': cart_subtotal
    }
    return render(request, 'cart_detail.html', context)

def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = Product.objects.filter(id=product_id, is_active=True).first()
        if not product:
            return render(request, '404.html', status=404)
        else:
            size = request.POST.get('size')
            color = request.POST.get('color')
            quantity = int(request.POST.get('quantity', 1))
            if quantity < product.stock:
                cart = Cart.objects.get_or_create(user=request.user)[0]
                item, created = CartItem.objects.get_or_create(cart=cart, product=product, size=size)
                if not created:
                    item.quantity += 1
                item.save()
                return redirect('cart:cart_detail')
                # item,created = CartItem.objects.create(cart=cart, product=product, size=size, quantity=quantity)
                # item.save()
                # return redirect('cart_detail')
    return render(request, 'cart_detail.html')


def remove_from_cart(request, product_id):
    if request.method == 'POST':
        product = Product.objects.filter(id=product_id, is_active=True).first()
        if not product:
            return render(request, '404.html', status=404)
        else:
            cart = Cart.objects.filter(user=request.user).first()
            if cart:
                item = CartItem.objects.filter(cart=cart, product=product).first()
                print(f"Removing item: {item} from cart: {cart}")
    return redirect('cart:cart_detail')

def clear_cart(request):
    if request.method == 'POST':
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart.items.all().delete()
    return redirect('cart:cart_detail')