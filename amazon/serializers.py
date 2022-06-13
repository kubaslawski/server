from rest_framework import serializers
from datetime import datetime

from .models import CustomUser, Category, Product


class CustomUserSerializer(serializers.ModelSerializer):
    last_login = serializers.DateTimeField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'last_login',
            'is_superuser',
            'is_staff',
            'is_active',
            'date_joined',
            'is_seller',
            'address',
        ]


class CategorySerializer(serializers.ModelSerializer):
    value = serializers.CharField(source='pk', read_only=True)
    label = serializers.CharField(source='title', read_only=True)

    class Meta:
        model = Category
        fields = [
            'value',
            'label'
        ]


class ProductSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(required=False)

    class Meta:
        model = Product
        fields = [
            'id',
            'seller',
            'category',
            'name',
            'description',
            'stock',
            'price',
            'photo'
        ]
