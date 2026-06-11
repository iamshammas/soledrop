from datetime import datetime, time
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from accounts.models import CustomUser
from products.models import Brand, Product, Variant
from orders.models import Coupon, Order, OrderItem
from django.db.models import F, Count, DecimalField, ExpressionWrapper, Sum
from django.contrib.auth import logout
from django.contrib import messages 
from .decorators import admin_required
# Create your views here.

@admin_required
def dashboard(request):
    orders = Order.objects.all()
    total_users = CustomUser.objects.filter(is_staff=False).count()
    total_products = Product.objects.count()
    recent_orders = Order.objects.order_by('-created_at')[:8]
    low_stock_variants = (Variant.objects
        .filter(stock__gt=0, stock__lte=5)
        .select_related('product')
        .order_by('stock')[:6]
    )
    top_products = (OrderItem.objects
        .values(
            name=F('variant__product__name')
        )
        .annotate(
            sold=Sum('quantity'),
            revenue=Sum(ExpressionWrapper(F('quantity') * F('price_at_purchase'),output_field=DecimalField()))
        )
        .order_by('-sold')[:5]
    )
    context = {
        'active_page'   :  'dashboard',
        'total_orders'  : orders.count(),
        'top_items' : OrderItem.objects.order_by('-quantity')[:5],
        'total_revenue':      orders.aggregate(t=Sum('total_amount'))['t'] or 0,
        'pending_orders': orders.filter(status='pending').count(),
        'shipped_orders': orders.filter(status='shipped').count(),
        'cancelled_orders': orders.filter(status='cancelled').count(),
        'confirmed_orders': orders.filter(status='confirmed').count(),
        'delivered_orders': orders.filter(status='delivered').count(),
        'total_users'   : total_users,
        'total_products': total_products,
        'recent_orders' : recent_orders,
        'low_stock_variants': low_stock_variants,
        'top_products' : top_products
    }
    return render(request, 'admin_panel/dashboard.html',context)

@admin_required
def variants(request):
    variants = Variant.objects.select_related('product').all()
    products = Product.objects.all()
    context = {
        'active_page': 'variants',
        'variants': variants,
        'variants_count': variants.count(),
        'products': products,
    }
    return render(request, 'admin_panel/variants.html', context)

@admin_required
def variant_add(request):
    if request.method == 'POST':
        product_id = request.POST.get('product') ## correct
        size = request.POST.get('size_value') ## correct
        stock = request.POST.get('stock')
        product = get_object_or_404(Product, id=product_id)
        Variant.objects.create(product=product, size=size, stock=stock)
        messages.success(request, f'Variant "{size}" added to "{product.name}" successfully.')
        return redirect('admin_panel:variants')
    return redirect('admin_panel:variants')

@admin_required
def variant_delete(request, variant_id):
    variant = get_object_or_404(Variant, id=variant_id)
    variant.delete()
    messages.info(request, f'Variant {variant.product.name} deleted successfully.')
    return redirect('admin_panel:variants')

@admin_required
def variant_edit(request, variant_id):
    variant = get_object_or_404(Variant, id=variant_id)
    if request.method == 'POST':
        product_id = request.POST.get('product')
        variant.product = get_object_or_404(Product,id=product_id)
        variant.size = request.POST.get('size_value')
        variant.stock = request.POST.get('stock')
        variant.save()
        return redirect('admin_panel:variants')
    return redirect('admin_panel:variants')

@admin_required
def orders(request):
    orders = Order.objects.select_related('user').order_by('-created_at')
    context = {
        'active_page': 'orders',
        'orders': orders,
        'orders_count': orders.count(),
    }
    return render(request, 'admin_panel/orders.html', context)

@admin_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    # for item in order.items.all():
    #     print(item)
    context = {
        'order': order,
    }
    return render(request, 'admin_panel/order_detail.html', context)

@admin_required
def order_update_status(request, order_id):
    order = get_object_or_404(Order,id=order_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        order.status = status
        order.save()
        messages.success(request, "Order status updated successfully.")
    return redirect('admin_panel:orders')


@admin_required 
def products(request):
    brands = Brand.objects.all()
    products = Product.objects.all()
    context = {
        'active_page': 'products',
        'brands': brands,
        'products': products,
        'products_count': products.count()
    }
    return render(request, 'admin_panel/products.html', context)

@admin_required
def product_add(request):
    if request.method == 'POST':
        print('ADD PRODUCT POST METHOD')
        name = request.POST.get('name')
        description = request.POST.get('description')
        brand_id = request.POST.get('brand')
        old_price = request.POST.get('old_price')
        new_price = request.POST.get('new_price')
        badge = request.POST.get('badge')
        image = request.FILES.get('image')
        is_active = request.POST.get('is_active', None) == 'on'
        is_featured = request.POST.get('is_featured', None) == 'on'
        brand = get_object_or_404(Brand, id=brand_id)
        Product.objects.create(
            name=name,
            description=description,
            brand=brand,
            old_price=old_price,
            new_price=new_price,
            badge=badge,
            image=image,
            is_active=is_active,
            is_featured=is_featured
        )
        return redirect('admin_panel:products')
    return redirect('admin_panel:products')

@admin_required
def product_edit(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'GET':
        return JsonResponse({
            'name': product.name,
            'description': product.description,
            'brand_id': product.brand_id,
            'old_price': str(product.old_price or ''),
            'new_price': str(product.new_price or ''),
            'badge': product.badge or '',
            'is_active': product.is_active,
            'is_featured': product.is_featured,
            'image_url': product.image.url if product.image else '',
        })
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        brand_id = request.POST.get('brand')
        product.old_price = request.POST.get('old_price')
        product.new_price = request.POST.get('new_price')
        product.badge = request.POST.get('badge')
        image = request.FILES.get('image')
        if image:   
            product.image = image
        product.is_active = request.POST.get('is_active', None) == 'on'
        product.is_featured = request.POST.get('is_featured', None) == 'on'
        if brand_id:
            product.brand = get_object_or_404(Brand, id=brand_id)
        product.save()
        return redirect('admin_panel:products')

@admin_required
def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('admin_panel:products')

@admin_required
def users(request):
    users = CustomUser.objects.annotate(order_count=Count('order')).order_by('-date_joined')
    return render(
        request,
        'admin_panel/users.html',
        {
            'users': users,
            'users_count': users.count(),
            'active_page': 'users',
        },
    )

@admin_required
def user_detail(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    recent_orders = Order.objects.filter(user=user).order_by('-created_at')[:10]
    return render(
        request,
        'admin_panel/user_detail.html',
        {
            'detail_user': user,
            'recent_orders': recent_orders,
            'user_orders_count': Order.objects.filter(user=user).count(),
            'active_page': 'users',
        },
    )

@admin_required
def toggle_user_status(request, user_id):   
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = not user.is_active
    user.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@admin_required
def brands(request):
    context = {
        'active_page': 'brands',
        'brands' : Brand.objects.all()
    }
    return render(request, 'admin_panel/brands.html', context)

@admin_required
def brand_add(request):
    if request.method == 'POST':
        brand_id = request.POST.get('brand_id')
        name = request.POST.get('name')
        image = request.FILES.get('image')
        active = int(request.POST.get('is_active', 0)) == 1
        
        if brand_id:
            brand = get_object_or_404(Brand, id=brand_id)
            brand.name = name
            brand.is_active = active
            brand.slug = brand.generate_slug()
            if image:
                brand.image = image
            brand.save()
        else:
            Brand.objects.create(name=name, image=image, is_active=active)
            
        return redirect('admin_panel:brands')
    return HttpResponse('hello')

@admin_required
def brand_delete(request, brand_id):
    brand = get_object_or_404(Brand, id=brand_id)
    brand.delete()
    return redirect('admin_panel:brands')

@admin_required
def coupons(request):
    coupons = Coupon.objects.all()
    context = {
        'active_page': 'coupons',
        'coupons' : coupons ,
        'coupons_count' : coupons.count() ,
    }
    return render(request, 'admin_panel/coupons.html',context)

@admin_required
def coupon_add(request):
    if request.method == 'POST':
        coupon_id = request.POST.get('coupon_id')
        code = request.POST.get('code')
        coupon_type = request.POST.get('coupon_type')
        discount = request.POST.get('discount')
        minimum_order_amount = request.POST.get('minimum_order_amount')
        usage_limit = request.POST.get('usage_limit')
        date_str = request.POST.get('expiration_date')
        expiration_date = datetime.combine(datetime.strptime(date_str, '%Y-%m-%d').date(),time(23, 59, 59))
        today = datetime.today()
        if expiration_date <= today:
            messages.error(request,"Expiration date must be later than today.")
            return redirect('admin_panel:coupon_add')
        
        if coupon_id:
            coupon = Coupon.objects.get(id=coupon_id)
            coupon.code = code
            coupon.coupon_type = coupon_type
            coupon.discount = discount
            coupon.minimum_order_amount = minimum_order_amount
            coupon.usage_limit = usage_limit
            coupon.expiration_date = expiration_date
            coupon.save()
            messages.success(request, "Coupon updated successfully.")
            return redirect('admin_panel:coupons')
        else:
            Coupon.objects.create(
                code = code,
                coupon_type = coupon_type,
                discount = discount,
                minimum_order_amount = minimum_order_amount,
                usage_limit = usage_limit,
                expiration_date = expiration_date
            )
            messages.success(request, "Coupon created successfully.")
            return redirect('admin_panel:coupons')

@admin_required
def coupon_delete(request,id):
    coupon = get_object_or_404(Coupon,id=id)
    coupon.delete()
    messages.success(request, "Coupon deleted successfully.")
    return redirect('admin_panel:coupons')

@admin_required
def admin_logout(request):
    logout(request)
    return redirect('accounts:home')

