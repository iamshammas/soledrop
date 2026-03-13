from django.shortcuts import render

# Create your views here.

def user_registration(request):
    if request.method == 'POST':
        # Handle user registration logic here
        pass
    return render(request, 'register.html')


def user_login(request):
    if request.method == 'POST':
        # Handle user login logic here
        pass
    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')