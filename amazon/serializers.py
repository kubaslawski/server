from rest_framework import serializers

from django.db.models import Avg, Sum
from django.contrib.auth import get_user_model

from .models import CustomUser, Category, Product, Rate, Basket, BasketItem, SubCategory, Address, PurchasedProduct

UserModel = get_user_model()


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = [
            'country',
            'state',
            'city',
            'street',
            'post_code'
        ]


class CustomUserSerializer(serializers.ModelSerializer):
    basket_count = serializers.SerializerMethodField(read_only=True)
    address = AddressSerializer()

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'basket_count',
            'address'
        ]

    def get_basket_count(self, obj):
        user = CustomUser.objects.get(email=obj)
        basket = Basket.objects.get(user=user)
        basket_count = BasketItem.objects.filter(basket=basket).aggregate(total_items=Sum('quantity'))
        return basket_count['total_items']


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


class SubCategorySerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(required=False)

    class Meta:
        model = SubCategory
        fields = [
            'id',
            'title',
            'photo'
        ]


class CategorySerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(required=False)
    sub_categories = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = [
            'title',
            'photo',
            'sub_categories',
            'pk'
        ]

    def get_sub_categories(self, obj):
        category = obj.pk
        sub_categories = SubCategory.objects.filter(category=category)
        serializer = SubCategorySerializer(sub_categories, many=True)
        return serializer.data


class ProductSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(required=False)
    category = CategorySerializer(read_only=True)
    sub_category = SubCategorySerializer()
    product_rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'category',
            'sub_category',
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
            'category',
            'name',
            'description',
            'stock',
            'price',
            'photo',
        ]


class ProductListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    sub_category = SubCategorySerializer(read_only=True)
    product_rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'category',
            'sub_category',
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


class BasketSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Basket
        fields = [
            'user'
        ]


class BasketItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = BasketItem
        fields = [
            'product',
            'quantity',
            'basket'
        ]


class ProductPurchasedSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = PurchasedProduct
        fields = [
            'product',
            'quantity'
        ]

