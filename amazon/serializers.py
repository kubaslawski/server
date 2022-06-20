from rest_framework import serializers

from django.db.models import Avg
from django.contrib.auth import get_user_model # If used custom user model

from .models import CustomUser, Category, Product, Rate

UserModel = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
        ]


class CreateCustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )

        return user

    class Meta:
        model = UserModel
        fields = ("id", "email", "password")

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("Password must have at least 6 characters")


class SellerSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
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
    seller = SellerSerializer(read_only=True, required=False)
    category = CategorySerializer(read_only=True)
    product_rating = serializers.SerializerMethodField(read_only=True)

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
            'photo',
            'product_rating'
        ]

    def get_product_rating(self, obj):
        rate = Rate.objects.filter(product=obj.pk)
        rate_count = rate.count()
        avg_rate = rate.aggregate(average_price=Avg('rate'))
        return {'avg_rate': avg_rate['average_price'], 'rate_count': rate_count}


class ProductAddSerializer(serializers.ModelSerializer):
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
            'photo',
        ]

