from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('', views.home, name='home'),
    path('register/',views.user_registration, name='register'),
    path('login/',views.user_login, name='login'), 
    ##################### Add more authentication-related URLs here (e.g., login, logout, password reset)
    
]
