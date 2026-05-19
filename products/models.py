from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import CustomUser
from autoslug import AutoSlugField


class Category(models.Model):
    def generate_slug(self):
        return self.name.lower().replace(' ', '-')

    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from=generate_slug, unique=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} and id={self.id}'
    
    @property
    def product_count(self):
        return self.products.filter(is_active=True).count()

class Product(models.Model):
    def generate_slug(self):
        return f'{self.category.name.lower()}-{self.name.lower()}'.replace(' ', '-')

    BADGE_CHOICES = [
    ('',     'None'),
    ('new',  'New'),
    ('sale', 'Sale'),
    ('hot',  'Hot'),
]
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from=generate_slug, unique=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='products', null=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    # stock = models.PositiveIntegerField(default=0)
    old_price = models.DecimalField(max_digits=10, decimal_places=2)
    new_price = models.DecimalField(max_digits=10, decimal_places=2)
    badge = models.CharField(max_length=20, choices=BADGE_CHOICES, default='',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

   
    @property
    def in_stock(self):
        res = self.available_variants.filter(stock__gt=0).exists()
        return res

    @property
    def available_stock(self):
        return sum(variant.stock for variant in self.available_variants.all())

    def __str__(self):
        return f'ID={self.id} -- {self.name}'
    
    class Meta:
        ordering = ['-created_at']
    
# class ProductSize(models.Model):
#     class Sizes(models.TextChoices):
#         six = '6', '6'
#         six_half = '6.5', '6.5'
#         seven = '7', '7'
#         seven_half = '7.5', '7.5'
#         eight = '8', '8'
#         eight_half = '8.5', '8.5'
#         nine = '9', '9'
#     product = models.ForeignKey(Product, on_delete=models.SET_NULL, related_name='available_sizes',null=True)
#     value = models.CharField(max_length=20, choices=Sizes.choices)

#     class Meta:
#         ordering = ['value']
#         unique_together = ('product', 'value')

#     def __str__(self):
#         # return f"ID={self.id} -- {self.product.name} - Size {self.value}"
#         return self.value

# class ProductColor(models.Model):
#     class Colors(models.TextChoices):
#         RED = 'red', 'Red'
#         BLUE = 'blue', 'Blue'
#         GREEN = 'green', 'Green'
#         BLACK = 'black', 'Black'
#         WHITE = 'white', 'White'
#         YELLOW = 'yellow', 'Yellow'
#         ORANGE = 'orange', 'Orange'
#         PURPLE = 'purple', 'Purple'
#         PINK = 'pink', 'Pink'
#         BROWN = 'brown', 'Brown'
#         GREY = 'grey', 'Grey'
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='available_colors')
#     value = models.CharField(max_length=20, choices=Colors.choices)

#     class Meta:
#         ordering = ['value']
#         unique_together = ('product', 'value')

#     def __str__(self):
#         if self.product:
#             return f"{self.product.name} - Color {self.value}"
#         return f"Orphan Color - {self.value}"

class Variant(models.Model):
    class Sizes(models.TextChoices):
        SIX = '6', '6'
        SIX_HALF = '6.5', '6.5'
        SEVEN = '7', '7'
        SEVEN_HALF = '7.5', '7.5'
        EIGHT = '8', '8'
        EIGHT_HALF = '8.5', '8.5'
        NINE = '9', '9'
    
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        related_name='available_variants'
    )
    size = models.CharField(
        max_length=20, 
        choices=Sizes.choices
    )
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('product', 'size')
        ordering = ['size']

    def __str__(self):        
        return f"ID={self.id} -- {self.product.name} - {self.size}"

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
        return f'{self.user} — {self.product.name} ({self.rating}★)'