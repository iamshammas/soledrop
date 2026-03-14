from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from .models import CustomUser

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
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('accounts:home')  # Redirect to a success page.
    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')

def profile(request):  
    return render(request, 'profile.html')

def profile_edit(request):
    # Placeholder for profile edit logic
    return render(request, 'profile_edit.html')

def wishlist(request):
    # Placeholder for wishlist logic
    return render(request, 'wishlist.html')

def user_logout(request):
    # Placeholder for logout logic
    return redirect('accounts:home')