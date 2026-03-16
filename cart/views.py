from django.shortcuts import render

# Create your views here.

def add_to_cart(request, product_id):
    # Logic to add the product to the cart
    if request.method == 'POST':
        # Here you would typically add the product to the user's cart in the database
        # For now, we'll just print the product ID to the console for debugging
        print(f"Adding product with ID {product_id} to cart")
    return render(request, 'cart_detail.html')