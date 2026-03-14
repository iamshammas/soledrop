from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name
    
class Product(models.Model):
    BADGE_CHOICES = [
    ('',     'None'),
    ('new',  'New'),
    ('sale', 'Sale'),
    ('hot',  'Hot'),
]
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    old_price = models.DecimalField(max_digits=10, decimal_places=2)
    new_price = models.DecimalField(max_digits=10, decimal_places=2)
    badge = models.CharField(max_length=20, choices=BADGE_CHOICES, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    in_stock = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sizes')
    value = models.CharField(max_length=20)
    in_stock = models.BooleanField(default=True)

    class Meta:
        ordering = ['value']
        unique_together = ('product', 'value')

    def __str__(self):
        return f"{self.product.name} - Size {self.value}"