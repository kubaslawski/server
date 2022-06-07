from rest_framework import generics, mixins
from rest_framework.response import Response

from .models import CustomUser, Product
from .serializers import CustomUserSerializer, ProductSerializer

from django.conf import settings
from django.conf.urls.static import static


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
    generics.GenericAPIView
    ):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        print(settings.MEDIA_URL)
        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request)
        return self.list(request)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


user_api_view = CustomUserAPIView.as_view()
product_api_view = ProductAPIView.as_view()
