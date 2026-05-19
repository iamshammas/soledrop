from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from accounts.models import CustomUser
from products.models import Category, Product, Variant
from orders.models import Order
from django.db.models import Count
from django.contrib.auth import logout

# Create your views here.

def dashboard(request):
    return render(request, 'admin_panel/dashboard.html')

def variants(request):
    variants = Variant.objects.select_related('product').all()
    products = Product.objects.all()
    context = {
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
        print('####################################')
        print(f"Product ID: {product_id}, Size: {size}, Stock: {stock}")
        print('####################################')
        # Variant.objects.create(product=product, name=name, price=price, stock=stock)
        return redirect('admin_panel:variants')
    return HttpResponse('Variant add page')

def variant_delete(request, variant_id):
    return HttpResponse(f'Variant delete page for variant ID: {variant_id}')

def orders(request):
    orders = Order.objects.select_related('user').order_by('-created_at')
    context = {
        'orders': orders,
        'orders_count': orders.count(),
    }
    return render(request, 'admin_panel/orders.html', context)

def order_detail(request, order_id):
    return render(request, 'admin_panel/order_detail.html', {'order_id': order_id})

def order_update_status(request):
    return HttpResponse('Order status updated')

def order_detail(request, order_id):
    print(f"Fetching details for order ID: {order_id}")
    return HttpResponse(f"Order details for order ID: {order_id}")

def products(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        'categories': categories,
        'products': products,
        'products_count': products.count()
    }
    return render(request, 'admin_panel/products.html', context)

def product_add(request):
    if request.method == 'POST':
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
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
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
    categories = Category.objects.all()
    return render(request, 'admin_panel/categories.html', {'categories': categories})

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
    return render(request, 'admin_panel/coupons.html')

def admin_logout(request):
    logout(request)
    return redirect('accounts:home')

