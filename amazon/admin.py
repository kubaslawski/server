from django.contrib import admin
from .models import Category, Product, Rate, CustomUser, SubCategory

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Rate)
admin.site.register(SubCategory)
