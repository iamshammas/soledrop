from django.conf import settings
from django.db import models
import uuid
from products.models import Product
# Create your models here.

import datetime as dt

def gen_id():
    result = dt.datetime.now().strftime('%Y%m%d%H%M%S')
    return f'ORD-{result}'

# print(gen_id())

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=10, decimal_places=2)
    expiration_date = models.DateTimeField()

    def __str__(self):
        return self.code
    

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending','Pending'),
        ('shipped','Shipped'),
        ('cancelled','Cancelled'),
        ('confirmed','Confirmed'),
        ('delivered','Delivered')
    ]
    class PaymentMethod(models.TextChoices):
        COD = 'COD','Cash on Delivery'
        ONLINE = 'ONLINE','Online Payment'

    order_id = models.CharField()
    order_uuuid = models.UUIDField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES,default='pending',max_length=10)
    total_amount = models.DecimalField(decimal_places=2,max_digits=10)
    payment_method = models.CharField(max_length=10,choices=PaymentMethod.choices)
    #address part
    name = models.CharField(max_length=80)
    email = models.EmailField()
    phone = models.CharField(max_length=12)
    address_line1 = models.CharField(max_length=60)
    address_line2 = models.CharField(max_length=60,blank=True)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=20)
    pincode = models.IntegerField()
    country = models.CharField(max_length=26)
    coupon_code = models.ForeignKey(Coupon,null=True,blank=True,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def gen_uuid():
        iid = uuid.uuid4
        print(iid)
        return iid
    

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"
    

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,related_name='order_item',null=True)
    price_at_purchase = models.DecimalField(decimal_places=2,max_digits=10)
    