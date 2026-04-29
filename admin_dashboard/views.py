from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from products.models import Category

# Create your views here.

def dashboard(request):
    return render(request, 'admin_panel/dashboard.html')

def orders(request):
    return render(request, 'admin_panel/orders.html')

def order_detail(request, order_id):
    return render(request, 'admin_panel/order_detail.html', {'order_id': order_id})

def products(request):
    return render(request, 'admin_panel/products.html')

def users(request):
    return render(request, 'admin_panel/users.html')

def categories(request):
    categories = Category.objects.all()
    return render(request, 'admin_panel/categories.html', {'categories': categories})

def category_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        active = int(request.POST.get('is_active')) == 1
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
    # Implement logout logic here
    pass

