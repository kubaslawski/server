from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from django.core.validators import MaxValueValidator, MinValueValidator


from .managers import CustomUserManager

RATE_CHOICES = [
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5')
]


def user_directory_path(instance, filename):
    return 'products/images/{0}'.format(filename)


def category_directory_path(instance, filename):
    return 'category/images/{0}'.format(filename)


def sub_category_directory_path(instance, filename):
    return 'subcategory/images/{0}'.format(filename)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    first_name = models.CharField(max_length=32, blank=True, null=True)
    last_name = models.CharField(max_length=32, blank=True, null=True)
    is_seller = models.BooleanField(default=False)
    address = models.ForeignKey("Address", on_delete=models.CASCADE, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


class Category(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    photo = models.ImageField(upload_to=category_directory_path, blank=True, null=True)

    def __str__(self):
        return self.title


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True, blank=True)
    photo = models.ImageField(upload_to=sub_category_directory_path, blank=True, null=True)

    def __str__(self):
        return self.title


class Rate(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField(max_length=512, null=True, blank=True)
    rate = models.IntegerField(choices=RATE_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=512, null=True, blank=True)
    stock = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ])
    price = models.FloatField()
    photo = models.ImageField(upload_to=user_directory_path, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.price = round(self.price, 2)
        super(Product, self).save(*args, **kwargs)


class Basket(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class BasketItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)


class Address(models.Model):
    country = models.CharField(max_length=32)
    state = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    street = models.CharField(max_length=64)
    post_code = models.CharField(_("post_code"), max_length=5)