from django.contrib import admin
from .models import Category, Product, Comment, CustomUser

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Comment)
