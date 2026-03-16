from django.contrib import admin

from products.models import Category, Product

# Register your models here.

admin.site.site_header = "SoleDrop Admin"
admin.site.site_title = "SoleDrop Admin Portal" 
admin.site.index_title = "Welcome to the SoleDrop Admin Portal"
admin.site.register(Category)
admin.site.register(Product)    