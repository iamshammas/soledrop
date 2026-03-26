from django.conf import settings
from django.db import models

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
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"