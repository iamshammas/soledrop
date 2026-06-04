from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import authenticate, login,logout
from products.models import Product
from .models import Address, CustomUser
from orders.models import Order
from cart.models import Cart
from django.contrib.auth.decorators import login_required

# Create your views here.

def user_registration(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        print(email)
        phone_number = request.POST.get('phone')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html')
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, "register.html")
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
        else:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'login.html')
    return render(request, 'login.html')

def home(request):
    # cart = Cart.objects.filter(user=request.user.id).first() if request.user.is_authenticated else None
    # if cart:
    #     cart_count = cart.items.count()
    #     cart_items = cart.items.all()
    #     cart_total = cart.total_price
    # else:
    #     cart_count = 0
    #     cart_items = []
    #     cart_total = 0
    # context = {
    #     'cart_count': cart_count,
    #     'cart_items':cart_items,
    #     'cart_total': cart_total
    # }
    return render(request, 'home.html')

@login_required
def profile(request):  
    # cart = Cart.objects.filter(user=request.user).first()
    # if cart:
    #     cart_count = cart.items.count()
    #     cart_items = cart.items.all()
    #     cart_total = cart.total_price
    # else:
    #     cart_count = 0
    #     cart_items = []
    #     cart_total = 0
    order_count = Order.objects.filter(user=request.user).count()
    wishlist_count = request.user.wishlist.count() if request.user.is_authenticated else 0
    recent_orders = Order.objects.filter(user=request.user).order_by('-created_at')[:3]
    context = {
        'order_count': order_count,
        'wishlist_count':wishlist_count,
        'recent_orders':recent_orders
    }
    return render(request, 'profile.html',context)

@login_required
def profile_edit(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone')
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.phone_number = phone_number
        user.save()
        return redirect('accounts:profile')
    return render(request, 'profile_edit.html')

def wishlist(request):
    wishlist_items = request.user.wishlist.all() if request.user.is_authenticated else []
    cart = Cart.objects.filter(user=request.user).first() if request.user.is_authenticated else None
    if cart:
        cart_count = cart.items.count()
        cart_items = cart.items.all()
        cart_total = cart.total_price
    else:
        cart_count = 0
        cart_items = []
        cart_total = 0
    context = {
        'wishlist_items': wishlist_items,
        'cart_count': cart_count,
        'cart_items': cart_items,
        'cart_total': cart_total
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

def address_list(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request,'addresses.html',{'addresses':addresses})
    # return HttpResponse('HELLO ADDRES')

def address_add(request):
    if request.method == 'POST':
        label = request.POST.get('label') 
        name = request.POST.get('full_name')
        phone_no = request.POST.get('phone_number')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pin_code')
        country = request.POST.get('country')
        is_default = request.POST.get('is_default') == 'on'

        if is_default:
            Address.objects.filter(
                user=request.user,
                is_default=True
            ).update(is_default=False)

        Address.objects.create(
            user=request.user,
            label=label,
            full_name=name,
            phone_number=phone_no,
            address=address,
            city=city,
            state=state,
            pin_code=pincode,
            country=country,
            is_default=is_default
        )
        return redirect('accounts:address_list')
    return render(request,'address_form.html')

def address_edit(request,id):
    address = get_object_or_404(Address,id=id,user=request.user)
    if request.method == 'POST':
        is_default = request.POST.get('is_default') == 'on'
        if is_default:
            Address.objects.filter(user=request.user,is_default=True).exclude(id=address.id).update(is_default=False)
        address.label = request.POST.get('label')
        address.full_name = request.POST.get('full_name')
        address.phone_number = request.POST.get('phone_number')
        address.address = request.POST.get('address')
        address.city = request.POST.get('city')
        address.state = request.POST.get('state')
        address.pin_code = request.POST.get('pin_code')
        address.country = request.POST.get('country')
        address.is_default = is_default

        address.save()
        return redirect('accounts:address_list')
    return render(request,'address_form.html',{'address':address})

def address_delete(request,id):
    address = get_object_or_404(Address,id=id,user=request.user)
    if request.method == 'POST':
        address.delete()
        messages.success(request, "Address deleted successfully.")
        return redirect('accounts:address_list')
    return redirect('accounts:address_list')

def user_logout(request):
    logout(request)
    return redirect('accounts:home')

def change_password(request):
    # if request.method ==
    # user = request.user
    # user.set_password("new_password")
    # user.save()
    return render(request, 'change_password.html')