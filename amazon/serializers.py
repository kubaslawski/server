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
    # seller_data = serializers.SerializerMethodField(read_only=True)
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

    # def get_seller_data(self, obj):
    #     email = None
    #     if obj.seller.email:
    #         email = obj.seller.email
    #     return {
    #         'email': email
    #     }
