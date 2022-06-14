from rest_framework import generics, mixins
from rest_framework.parsers import FormParser, MultiPartParser

from .models import CustomUser, Product, Category
from .serializers import CustomUserSerializer, ProductSerializer, CategorySerializer, ProductAddSerializer

from django.shortcuts import get_object_or_404


class CustomUserAPIView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
    ):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request)
        return self.list(request)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ProductAPIView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView
    ):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        category_pk = kwargs.get('category_pk')
        if category_pk:
            self.queryset = Product.objects.filter(category=category_pk)
            return self.list(request)
        if pk:
            return self.retrieve(request)
        return self.list(request)

    def post(self, request, *args, **kwargs):
        self.serializer_class = ProductAddSerializer
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        self.serializer_class = ProductAddSerializer
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk is not None:
            product = get_object_or_404(Product, pk=pk)
            if product.photo:
                product.photo.delete()
        return self.destroy(request, *args, **kwargs)


class CategoryAPIView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView
    ):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk is not None:
            obj = get_object_or_404(pk=pk)
            if obj:
                return self.retrieve(request)
        return self.list(request)


user_api_view = CustomUserAPIView.as_view()
product_api_view = ProductAPIView.as_view()
category_api_view = CategoryAPIView.as_view()
