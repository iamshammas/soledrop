from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import CustomUser

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
    
    @property
    def product_count(self):
        return self.products.filter(is_active=True).count()

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
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='products', null=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    old_price = models.DecimalField(max_digits=10, decimal_places=2)
    new_price = models.DecimalField(max_digits=10, decimal_places=2)
    badge = models.CharField(max_length=20, choices=BADGE_CHOICES, default='',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    @property
    def in_stock(self):
        res = self.variants.filter(stock__gt=0).exists()
        return res

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']
    
class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, related_name='sizes',null=True)
    value = models.CharField(max_length=20)

    class Meta:
        ordering = ['value']
        unique_together = ('product', 'value')

    def __str__(self):
        return f"{self.product.name} - Size {self.value}"

class ProductColor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, related_name='available_colors',null=True)
    value = models.CharField(max_length=20)

    class Meta:
        ordering = ['value']
        unique_together = ('product', 'value')

    def __str__(self):
        return f"{self.product.name} - Color {self.value}"

class Variant(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='variants')
    color = models.ForeignKey(ProductColor,  on_delete=models.CASCADE)
    size = models.ForeignKey(ProductSize,on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('product', 'color', 'size')
        ordering = ['product', 'color', 'size']

    def __str__(self):        
        return f"{self.product.name} - {self.color.value} - {self.size.value}"

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('product', 'user')

    def __str__(self):
        return f'{self.user.username} — {self.product.name} ({self.rating}★)'