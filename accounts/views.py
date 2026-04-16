from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from products.models import Product
from .models import CustomUser
from cart.models import Cart
from django.contrib.auth.decorators import login_required

# Create your views here.

def user_registration(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            return render(request, 'register.html', {'error': 'Passwords do not match.'})
        # Create the user
        user = CustomUser.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            password=password1
        )
        if user is not None:
            user.save()
            return render(request, 'login.html', {'success': 'Account created successfully. Please log in.'})
    return render(request, 'register.html')


def user_login(request):
    if request.user.is_authenticated:
        return redirect('accounts:home')
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('accounts:home')  
    return render(request, 'login.html')

def home(request):
    cart = Cart.objects.filter(user=request.user.id).first() if request.user.is_authenticated else None
    cart_count = cart.items.count() if cart else 0

    context = {
        'cart_count': cart_count
    }
    return render(request, 'home.html',context)

@login_required
def profile(request):  
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        cart_count = cart.items.count()
        cart_items = cart.items.all()
    else:
        cart_count = 0
        cart_items = []
    context = {
        'cart_count': cart_count,
        'cart_items': cart_items,
    }
    return render(request, 'profile.html', context)

@login_required
def profile_edit(request):
    # Placeholder for profile edit logic
    return render(request, 'profile_edit.html')

def wishlist(request):
    wishlist_items = request.user.wishlist.all() if request.user.is_authenticated else []
    cart = Cart.objects.filter(user=request.user).first() if request.user.is_authenticated else None
    cart_count = cart.items.count() if cart else 0
    cart_items = cart.items.all() if cart else []
    context = {
        'wishlist_items': wishlist_items,
        'cart_count': cart_count,
        'cart_items': cart_items,

    }
    return render(request, 'wishlist.html', context)

@login_required
def wishlist_toggle(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        if product in request.user.wishlist.all():
            request.user.wishlist.remove(product)
        else:
            request.user.wishlist.add(product)
        next = request.POST.get('next', '/')
        return redirect(next)
    return redirect('accounts:home')

@login_required
def clear_wishlist(request):
    if request.method == 'POST':
        request.user.wishlist.clear()
    return redirect('accounts:wishlist')

def user_logout(request):
    logout(request)
    return redirect('accounts:home')

def change_password(request):
    # Placeholder for change password logic
    return render(request, 'change_password.html')