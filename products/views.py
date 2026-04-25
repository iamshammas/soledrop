from django.shortcuts import render
from .models import Category, Product
from django.core.paginator import Paginator
from cart.models import Cart
from django.contrib.auth.decorators import login_required

def product_list(request):
    print(request.GET.get('category'))
    all_categories = Category.objects.filter(is_active=True)
    qs = Product.objects.filter(is_active=True)
    paginator = Paginator(qs, 8)  
    page_obj = paginator.get_page(request.GET.get('page', 1))
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        cart = None
    if cart:    
        cart_count = cart.items.count()
        cart_items = cart.items.all()
        cart_total = cart.total_price
    else:
        cart_count = 0
        cart_items = []
        cart_total = 0
    context = {
        'all_categories': all_categories,
        'paginator': paginator,
        'page_obj': page_obj,
        'cart_count': cart_count,
        'cart_items': cart_items,
        'cart_total': cart_total,
    }
    return render(request, 'product_list.html', context)

@login_required
def home_page(request):
    categories = Category.objects.filter(is_active=True)
    featured_products = Product.objects.filter(is_active=True, is_featured=True)
    # cart = Cart.objects.filter(user=request.user).first()
    # if cart:
    #     cart_count = cart.items.count()
    #     cart_items = cart.items.all()
    #     cart_total = cart.total_price
    # else:
    #     cart_count = 0
    #     cart_items = []
    #     cart_total = 0
    # cart_items = []
    context = {
        'categories': categories,
        'featured_products': featured_products,
        # 'cart_count': cart_count,
        # 'cart_items': cart_items,
        # 'cart_total':cart_total
    }
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

 