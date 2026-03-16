from itertools import product

from django.shortcuts import render

from products.models import Product

# Create your views here.

def cart_detail(request):
    # Logic to display the cart details
    return render(request, 'cart_detail.html')

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
                # Here you would typically add the product to the user's cart in the database
                print(f"Adding product '{product.name}' (ID: {product_id}) to cart with size '{size}', color '{color}', and quantity {quantity}")
    return render(request, 'cart_detail.html')