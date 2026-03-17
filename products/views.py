from django.shortcuts import render
from .models import Category, Product
from django.core.paginator import Paginator
from cart.models import Cart

# Create your views here.

def product_list(request):
    all_categories = Category.objects.filter(is_active=True)
    qs = Product.objects.filter(is_active=True)
    paginator = Paginator(qs, 8)  
    page_obj = paginator.get_page(request.GET.get('page', 1))
    cart_count = Cart.objects.filter(user=request.user).first().items.count() if request.user.is_authenticated else 0
    cart_items = Cart.objects.filter(user=request.user).first().items.all() if request.user.is_authenticated else []
    context = {
        'all_categories': all_categories,
        'paginator': paginator,
        'page_obj': page_obj,
        'cart_count': cart_count,
        'cart_items': cart_items,
    }
    return render(request, 'product_list.html', context)

def home_page(request):
    categories = Category.objects.filter(is_active=True)
    featured_products = Product.objects.filter(is_active=True, is_featured=True)
    cart_count = Cart.objects.filter(user=request.user).first().items.count() if request.user.is_authenticated else 0
    context = {
        'categories': categories,
        'featured_products': featured_products,
        'cart_count': cart_count,
    }
    # print(f"Featured Products: {featured_products[0].image if featured_products else 'None'}")  # Debugging statement to check the featured products queryset
    return render(request, 'home.html', context)

def deals(request):
    return render(request, 'deals.html')


def product_detail(request, slug):
    product = Product.objects.filter(slug=slug, is_active=True).first()
    if not product:
        return render(request, '404.html', status=404)
    
    context = {
        'product': product,
    }
    return render(request, 'product_detail.html', context)
