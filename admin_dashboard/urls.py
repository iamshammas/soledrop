from django.urls import path
from . import views

app_name = 'admin_panel'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    
    # Orders 
    path('orders/', views.orders, name='orders'),
    path('orders/update-status/<uuid:order_id>/', views.order_update_status, name='order_update_status'),
    path('orders/<uuid:order_id>/detail/', views.order_detail, name='order_detail'),

    # Variants
    path('variants/', views.variants, name='variants'),
    path('variants/add/', views.variant_add, name='variant_add'),
    path('variants/<int:variant_id>/edit/', views.variant_edit, name='variant_edit'),
    path('variants/<int:variant_id>/delete/', views.variant_delete, name='variant_delete'),

    # Products
    path('products/', views.products, name='products'),
    path('products/add/', views.product_add, name='product_add'),
    path('products/<int:product_id>/edit/', views.product_edit, name='product_edit'),
    path('products/<int:product_id>/delete/', views.product_delete, name='product_delete'),

    # Users
    path('users/', views.users, name='users'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('toggle_user_status/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),

    # Categories
    path('categories/', views.categories, name='categories'),
    path('categories/add/', views.category_add, name='category_add'),
    path('categories/<int:category_id>/delete/', views.category_delete, name='category_delete'),

    # Coupons
    path('coupons/', views.coupons, name='coupons'),

    # Auth
    path('logout/', views.admin_logout, name='logout'),
]
