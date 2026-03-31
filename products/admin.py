from django.contrib import admin

from products.models import Category, Product, ProductSize, ProductColor, Variant

# Register your models here.

admin.site.site_header = "SoleDrop Admin"
admin.site.site_title = "SoleDrop Admin Portal" 
admin.site.index_title = "Welcome to the SoleDrop Admin Portal"
admin.site.register(Category)
admin.site.register(Product)    
admin.site.register(Variant)
admin.site.register(ProductSize)
admin.site.register(ProductColor)