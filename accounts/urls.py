from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('', views.home, name='home'),
    path('auth/register/',views.user_registration, name='register'),
    path('auth/login/',views.user_login, name='login'), 
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),  # Placeholder for profile edit view
    path('wishlist/', views.wishlist, name='wishlist'),  # Placeholder for wishlist view
    path('wishlist/clear/', views.clear_wishlist, name='wishlist_clear'),  # Placeholder for wishlist clear view
    path('wishlist/<int:product_id>/', views.wishlist_toggle, name='wishlist_toggle'),  # Placeholder for wishlist toggle view
    # path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name
    path('logout/', views.user_logout, name='logout'),  # Placeholder for logout view
    path('profile/change-password/', views.change_password, name='change_password'),  # Placeholder for change password view
    ##################### Add more authentication-related URLs here (e.g., login, logout, password reset)
]
