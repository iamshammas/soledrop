from django.contrib.auth.views import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from products.models import Variant
from cart.models import Cart, CartItem
from products.models import Product


@login_required
def cart_detail(request):
    # cart_items = Cart.objects.filter(user=request.user).first().items.all()
    cart = Cart.objects.get(user=request.user)
    context = {
        # 'cart_items': cart_items,
        # 'cart_count': cart_count,
        'cart_subtotal': cart.subtotal
    }
    return render(request, 'cart_detail.html', context)
 
def add_to_cart(request):
    if request.method == 'POST':
        variant_id = request.POST.get("variant_id")
        variant=get_object_or_404(Variant,id=variant_id)
        if not variant:
            return render(request, '404.html', status=404)
        else:
            cart = Cart.objects.get_or_create(user=request.user)[0]
            item, created = CartItem.objects.get_or_create(cart=cart, variant=variant)
            messages.success(request,'Added to cart')
            if not created:
                item.quantity += 1
                item.save()
                return redirect('cart:cart_detail')
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
                messages.warning(request,'Item deleted')
                cart_item.delete()
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
            # print('Item not found in cart')
            return render(request, '404.html', status=404)
        else:
            messages.success(request, "Item removed from cart.")
            item.delete()
            # print('HELOOOe$$$$')    
            # messages.info(request, "Item removed from cart.")
    return redirect('cart:cart_detail')

def clear_cart(request):
    if request.method == 'POST':
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart.items.all().delete()
            messages.info(request,'Cart Cleared')
    return redirect('cart:cart_detail')