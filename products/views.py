from django.shortcuts import render
from .models import Brand, Product
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib.auth.decorators import login_required

def product_list(request):
    all_brands = Brand.objects.filter(is_active=True).annotate(product_count=Count('products'))
    brand = None
    brand_slug = request.GET.get('brand')

    # Brand filter
    if brand_slug:
        brand = Brand.objects.filter(slug=brand_slug, is_active=True).first()
        if brand:
            qs = brand.products.filter(is_active=True)
        else:
            qs = Product.objects.filter(is_active=True)
    else:
        qs = Product.objects.filter(is_active=True)
    
    # price filter
    max_price = request.GET.get('max_price')

    if max_price:
        qs = qs.filter(new_price__lte=max_price)


    # Sorting
    current_sort = request.GET.get('sort', 'newest')
    if current_sort == 'price_low':
        qs = qs.order_by('new_price')

    elif current_sort == 'price_high':
        qs = qs.order_by('-new_price')

    elif current_sort == 'name':
        qs = qs.order_by('name')

    else:
        qs = qs.order_by('-id')  

    # Stock filter
    stock_filter = request.GET.get('stock')

    if stock_filter == 'inStock':
        qs = qs.filter(available_variants__stock__gt=0).distinct()

    elif stock_filter == 'sale':
        qs = qs.filter(badge='sale')

    elif stock_filter == 'new':
        qs = qs.filter(badge='new')

    elif stock_filter == 'hot':
        qs = qs.filter(badge='hot')

    paginator = Paginator(qs, 8)  
    page_obj = paginator.get_page(request.GET.get('page', 1))
    context = {
        'all_brands': all_brands,
        'paginator': paginator,
        'page_obj': page_obj,
        'current_brand': brand.name if brand else None,
        'current_sort': current_sort,
        'sort_options': [
            ('newest', 'Newest'),
            ('price_low', 'Price: Low to High'),
            ('price_high', 'Price: High to Low'),
            ('name', 'Name'),
        ],
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

 