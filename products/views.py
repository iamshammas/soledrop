from django.shortcuts import render

# Create your views here.

def product_list(request):
    # This is a placeholder view. You can replace it with actual logic to fetch and display products.
    return render(request, 'product_list.html')

def home_page(request):
    return render(request, 'home.html')