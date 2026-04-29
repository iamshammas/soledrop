from django.urls import path
from . import views

app_name = 'admin_panel'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    
    # Orders 
    path('orders/', views.orders, name='orders'),
    path('orders/<int:order_id>/', views.order_detail, name='admin_order_detail'),
    # path('orders/update-status/', views.order_update_status, name='admin_order_update_status'),

    # Products
    path('products/', views.products, name='products'),

    # Users
    path('users/', views.users, name='users'),

    # Categories
    path('categories/', views.categories, name='categories'),
    path('categories/add/', views.category_add, name='category_add'),
    path('categories/<int:category_id>/delete/', views.category_delete, name='category_delete'),

    # Coupons
    path('coupons/', views.coupons, name='coupons'),

    # Auth
    path('logout/', views.admin_logout, name='logout'),
]