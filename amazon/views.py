from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser

from .models import CustomUser, Product
from .serializers import CustomUserSerializer, ProductSerializer

from django.conf import settings
from django.conf.urls.static import static
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
        if pk is not None:
            return self.retrieve(request)
        return self.list(request)

    def post(self, request, *args, **kwargs):
        print(request.data)
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk is not None:
            product = get_object_or_404(Product, pk=pk)
            if product.photo:
                product.photo.delete()
        return self.destroy(request, *args, **kwargs)

user_api_view = CustomUserAPIView.as_view()
product_api_view = ProductAPIView.as_view()
