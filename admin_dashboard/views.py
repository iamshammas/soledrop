from django.shortcuts import render

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
    return render(request, 'admin_panel/categories.html')

def coupons(request):
    return render(request, 'admin_panel/coupons.html')

def admin_logout(request):
    # Implement logout logic here
    pass

