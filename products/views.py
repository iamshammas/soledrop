from django.shortcuts import render

# Create your views here.

def product_list(request):
    # This is a placeholder view. You can replace it with actual logic to fetch and display products.
    print(request.user)  # This will print the user information to the console for debugging purposes.
    return render(request, 'product_list.html')

def home_page(request):
    print(request.user)  # This will print the user information to the console for debugging purposes.
    return render(request, 'home.html')

def deals(request):
    return render(request, 'deals.html')

