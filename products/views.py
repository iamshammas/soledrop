from django.shortcuts import render
from .models import Brand, Product
from django.core.paginator import Paginator
from cart.models import Cart
from django.contrib.auth.decorators import login_required

def product_list(request):
    all_brands = Brand.objects.filter(is_active=True)
    brand_slug = request.GET.get('brand')
    if brand_slug:
        brand = Brand.objects.filter(slug=brand_slug, is_active=True).first()
        if brand:
            qs = brand.products.filter(is_active=True)
        else:
            qs = Product.objects.filter(is_active=True)
    else:
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
        cart_total = cart.total
    else:
        cart_count = 0
        cart_items = []
        cart_total = 0
    context = {
        'all_brands': all_brands,
        'paginator': paginator,
        'page_obj': page_obj,
        'cart_count': cart_count,
        'cart_items': cart_items,
        'cart_total': cart_total,
    }
    return render(request, 'product_list.html', context)

def home_page(request):
    brands = Brand.objects.filter(is_active=True)
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
        'brands': brands,
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

 