from django.db import models

# Create your models here.

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=10, decimal_places=2)
    expiration_date = models.DateTimeField()

    def __str__(self):
        return self.code