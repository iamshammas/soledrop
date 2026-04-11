from django.db import models
from accounts.models import CustomUser
from products.models import Product, Variant

# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    def __str__(self):
        return f"Cart of {self.user.email} with {self.total_items} items"



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Variant, on_delete=models.CASCADE)
    size = models.CharField(max_length=10)  
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cart', 'product', 'size')  # Ensure one entry per product-size in cart  

    @property
    def total_price(self):
        return self.product.new_price * self.quantity  # Use new_price for total calculation

    @property
    def in_stock(self):
        print(self.product.stock)
        return self.quantity <= self.product.stock

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Size: {self.size}) in {self.cart.user.email}'s Cart"