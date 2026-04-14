from django.conf import settings
from django.db import models
import uuid
from products.models import Variant
# Create your models here.

# import datetime as dt

# def gen_id():
#     result = dt.datetime.now().strftime('%Y%m%d%H%M%S')
#     return f'ORD-{result}'

# print(gen_id())

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=10, decimal_places=2)
    expiration_date = models.DateTimeField()

    def __str__(self):
        return self.code
    

class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending','Pending'
        SHIPPED = 'shipped','Shipped'
        CANCELLED = 'cancelled','Cancelled'
        CONFIRMED = 'confirmed','Confirmed'
        DELIVERED = 'delivered','Delivered'
    
    class PaymentMethod(models.TextChoices):
        COD = 'COD','Cash on Delivery'
        ONLINE = 'ONLINE','Online Payment'

    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(choices=Status.choices,default='pending',max_length=10)
    payment_method = models.CharField(max_length=10,choices=PaymentMethod.choices)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    #address part
    name = models.CharField(max_length=80)
    email = models.EmailField()
    phone = models.CharField(max_length=12)
    address_line1 = models.TextField()
    address_line2 = models.TextField(blank=True)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=20)
    pincode = models.CharField(max_length=10)
    country = models.CharField(max_length=26)
    coupon_code = models.ForeignKey(Coupon,null=True,blank=True,on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"Order #{self.id} by {self.user.first_name} {self.user.last_name}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='items',null=True)
    variant = models.ForeignKey(Variant, on_delete=models.SET_NULL,related_name='order_items',null=True)
    quantity = models.PositiveIntegerField()
    price_at_purchase = models.DecimalField(decimal_places=2,max_digits=10)
    
    @property
    def total_price(self):
        return self.price_at_purchase * self.quantity
    
    def __str__(self):
        return f"Item {self.id} of Order {self.order_id}"