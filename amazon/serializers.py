from rest_framework import serializers
from datetime import datetime

from .models import CustomUser, Category, Comment, Product


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


class ProductSerializer(serializers.ModelSerializer):
    seller = CustomUserSerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'category',
            'seller',
            'name',
            'description',
            'stock',
            'price',
            'photo'
        ]