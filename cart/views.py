from itertools import product

from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import redirect, render

from products.models import Product, Variant
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

def add_to_cart(request):
    if request.method == 'POST':
        item = request.POST.get('product_id')
        size = request.POST.get('size')
        print(item)
        print(size)
        variant = Variant.objects.filter(product=item,size=size)
        # print(variant)
        if not variant:
            print('Variant not found')
            return render(request, '404.html', status=404)
        else:
            # size = request.POST.get('size')
            # quantity = int(request.POST.get('quantity', 1))
            # if quantity < variant.stock:
            cart = Cart.objects.get_or_create(user=request.user)[0]
            item, created = CartItem.objects.get_or_create(cart=cart, variant=variant)
            if not created:
                item.quantity += 1
                item.save()
                return redirect('cart:cart_detail')
                # item,created = CartItem.objects.create(cart=cart, product=product, size=size, quantity=quantity)
                # item.save()
            return redirect('cart:cart_detail')
    return render(request, 'cart_detail.html')

def update_cart(request,item_id):
    if request.method == 'POST':
        cart_item = CartItem.objects.filter(id=item_id).first() 
        action = request.POST.get('action')
        if action == 'increase':
            # print(f'cart_item: {cart_item} and qty is {cart_item.quantity} and stock is {cart_item.product.stock}')
            # print(cart_item.product.stock)
            # print(cart_item.quantity)
            # if cart_item.quantity < cart_item.product.stock:
                # print('If  increase condition passed')
                # print(type(cart_item.product.stock))
            cart_item.quantity += 1
            cart_item.save()
            # else:
                # return render(request, '404.html')
            return redirect('cart:cart_detail')
        elif action == 'decrease':
            # print(cart_item.in_stock)
            # if cart_item.quantity > 1:
                # print('If condition passed')
            if cart_item.quantity == 1:
                print('Cart quantity is 1, removing item from cart')
                # Should implemenet a confirmation step here before deletion in a real application
                return redirect('cart:cart_detail')
            else:
                cart_item.quantity -= 1
                cart_item.save()
            return redirect('cart:cart_detail')


def remove_from_cart(request, product_id):
    if request.method == 'POST':
        # product = Product.objects.filter(id=product_id, is_active=True).first()
        item = CartItem.objects.filter(id=product_id,cart__user=request.user).first()
        # print(item)
        if not item:
            print('Item not found in cart')
            return render(request, '404.html', status=404)
        else:
            item.delete()
    return redirect('cart:cart_detail')

def clear_cart(request):
    if request.method == 'POST':
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart.items.all().delete()
    return redirect('cart:cart_detail')