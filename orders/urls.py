from django.urls import path
from . import views

app_name = 'orders'
urlpatterns = [
    # path('', views.order_history, name='order_history'),
    # path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/<uuid:order_id>/', views.order_confirmation, name='order_confirmation'),   
    path('apply-coupon/', views.apply_coupon, name='apply_coupon'),

]


# orders/checkout/        → checkout page (GET) + place order (POST)
# orders/confirmation/    → thank you page after order placed
# orders/                 → order history
# orders/<id>/            → order detail

