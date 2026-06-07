from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from accounts.models import CustomUser
from products.models import Category, Product, Variant
from orders.models import Order
from django.db.models import Count, Sum
from django.contrib.auth import logout
from django.contrib import messages 

# Create your views here.

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
    context = {
        'active_page'   :  'dashboard',
        'total_orders'  : orders.count(),
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
    }
    return render(request, 'admin_panel/dashboard.html',context)

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

def variant_delete(request, variant_id):
    variant = get_object_or_404(Variant, id=variant_id)
    variant.delete()
    messages.info(request, f'Variant {variant.product.name} deleted successfully.')
    return redirect('admin_panel:variants')

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

def orders(request):
    orders = Order.objects.select_related('user').order_by('-created_at')
    context = {
        'active_page': 'orders',
        'orders': orders,
        'orders_count': orders.count(),
    }
    return render(request, 'admin_panel/orders.html', context)

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    # for item in order.items.all():
    #     print(item)
    context = {
        'order': order,
    }
    return render(request, 'admin_panel/order_detail.html', context)

def order_update_status(request, order_id):
    order = get_object_or_404(Order,id=order_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        order.status = status
        order.save()
        messages.success(request, "Order status updated successfully.")
    return redirect('admin_panel:orders')


def products(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        'active_page': 'products',
        'categories': categories,
        'products': products,
        'products_count': products.count()
    }
    return render(request, 'admin_panel/products.html', context)

def product_add(request):
    if request.method == 'POST':
        print('ADD PRODUCT POST METHOD')
        name = request.POST.get('name')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        old_price = request.POST.get('old_price')
        new_price = request.POST.get('new_price')
        badge = request.POST.get('badge')
        image = request.FILES.get('image')
        is_active = request.POST.get('is_active', None) == 'on'
        is_featured = request.POST.get('is_featured', None) == 'on'
        category = get_object_or_404(Category, id=category_id)
        Product.objects.create(
            name=name,
            description=description,
            category=category,
            old_price=old_price,
            new_price=new_price,
            badge=badge,
            image=image,
            is_active=is_active,
            is_featured=is_featured
        )
        return redirect('admin_panel:products')
    return redirect('admin_panel:products')

def product_edit(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'GET':
        return JsonResponse({
            'name': product.name,
            'description': product.description,
            'category_id': product.category_id,
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
        category_id = request.POST.get('category')
        product.old_price = request.POST.get('old_price')
        product.new_price = request.POST.get('new_price')
        product.badge = request.POST.get('badge')
        image = request.FILES.get('image')
        if image:   
            product.image = image
        product.is_active = request.POST.get('is_active', None) == 'on'
        product.is_featured = request.POST.get('is_featured', None) == 'on'
        if category_id:
            product.category = get_object_or_404(Category, id=category_id)
        product.save()
        return redirect('admin_panel:products')

def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('admin_panel:products')

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

def toggle_user_status(request, user_id):   
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = not user.is_active
    user.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))


def categories(request):
    context = {
        'active_page': 'categories',
        'categories' : Category.objects.all()
    }
    return render(request, 'admin_panel/categories.html', context)

def category_add(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        name = request.POST.get('name')
        image = request.FILES.get('image')
        active = int(request.POST.get('is_active', 0)) == 1
        
        if category_id:
            category = get_object_or_404(Category, id=category_id)
            category.name = name
            category.is_active = active
            category.slug = category.generate_slug()
            if image:
                category.image = image
            category.save()
        else:
            Category.objects.create(name=name, image=image, is_active=active)
            
        return redirect('admin_panel:categories')
    return HttpResponse('hello')

def category_delete(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect('admin_panel:categories')

def coupons(request):
    context = {
        'active_page': 'coupons',
    }
    return render(request, 'admin_panel/coupons.html',context)

def admin_logout(request):
    logout(request)
    return redirect('accounts:home')

