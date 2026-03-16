from django.shortcuts import render
from .models import Category, Product

# Create your views here.

def product_list(request):
    all_categories = Category.objects.filter(is_active=True)
    context = {
        'all_categories': all_categories,
    }
    return render(request, 'product_list.html', context)

def home_page(request):
    categories = Category.objects.filter(is_active=True)
    featured_products = Product.objects.filter(is_active=True, is_featured=True)
    context = {
        'categories': categories,
        'featured_products': featured_products,
    }
    print(f"Featured Products: {featured_products[0].image if featured_products else 'None'}")  # Debugging statement to check the featured products queryset
    return render(request, 'home.html', context)

def deals(request):
    return render(request, 'deals.html')

