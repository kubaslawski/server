from rest_framework import generics, mixins
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView

# authentication
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# internal
from .models import (
    CustomUser,
    Product,
    Category,
    Basket,
    BasketItem,
    PurchasedProduct,
    Rate
)
from .serializers import (
    CustomUserSerializer,
    CreateCustomUserSerializer,
    ProductSerializer,
    SingleProductSerializer,
    ProductListSerializer,
    ProductAddSerializer,
    CategorySerializer,
    BasketItemSerializer,
    ProductPurchasedSerializer,
    RateSerializer,
    RateAddSerializer,
)
# django
from django.shortcuts import get_object_or_404


class CreateUserAPIView(generics.CreateAPIView):
    # queryset = CustomUser.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    authentication_classes = []
    serializer_class = CreateCustomUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = CustomUser.objects.create_user(
            email=email,
            password=password
        )
        return Response({
            'email': user.email,
        })


class CustomUserAPIView(
    mixins.RetrieveModelMixin,
    generics.GenericAPIView
    ):
    serializer_class = CustomUserSerializer

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            self.queryset = CustomUser.objects.get(pk=pk)
            return self.retrieve(request)
        else:
            email = request.user
            user = CustomUser.objects.get(email=email)
            return Response({'user': user})


class CustomUserByTokenAPIView(
    generics.GenericAPIView
    ):

    def get(self, request, *args, **kwargs):
        email = request.user
        user = get_object_or_404(CustomUser, email=email)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)


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
        self.serializer_class = ProductListSerializer
        pk = kwargs.get('pk')
        category_pk = kwargs.get('category_pk')
        if category_pk:
            self.queryset = Product.objects.filter(category=category_pk)
            return self.list(request)
        if pk:
            self.serializer_class = SingleProductSerializer
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
    permission_classes = []
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk is not None:
            obj = get_object_or_404(pk=pk)
            if obj:
                return self.retrieve(request)
        return self.list(request)


class BasketAPIView(
    generics.GenericAPIView,
    mixins.ListModelMixin,
):
    serializer_class = BasketItemSerializer

    def get(self, request, *args, **kwargs):
        email = request.user
        user = CustomUser.objects.get(email=email)
        basket = Basket.objects.get(user=user)
        self.queryset = BasketItem.objects.filter(basket=basket)
        return self.list(request, *args, **kwargs)

    # 1. Check if basket exists
    # 2. If not - create a basket, then create product in basket
    # 3. If does - check if product is already in the basket

    def post(self, request, *args, **kwargs):
        product_id = request.data['product']
        product = Product.objects.get(pk=product_id)
        quantity = int(request.data['quantity'])
        user = CustomUser.objects.get(email=request.user)
        user_basket = Basket.objects.filter(user=user).first()
        if not user_basket:
            user_basket = Basket.objects.create(
                user=user
            )
            user_basket.save()
            basket_item = BasketItem.objects.create(
                basket=user_basket,
                product=product,
                quantity=quantity
            )
            basket_item.save()
            items = BasketItem.objects.filter(basket=user.id)
            serializer = BasketItemSerializer(items, many=True)
            return Response(serializer.data)
        else:
            basket_product = BasketItem.objects.filter(basket=user_basket, product=product).first()
            if basket_product:
                basket_product.quantity = basket_product.quantity + quantity
                basket_product.save()
                if basket_product.quantity == 0:
                    basket_product.delete()
                user = CustomUser.objects.get(email=request.user)
                items = BasketItem.objects.filter(basket=user_basket)
                serializer = BasketItemSerializer(items, many=True)
                return Response(serializer.data)
            else:
                basket_item = BasketItem.objects.create(
                    basket=user_basket,
                    product=product,
                    quantity=quantity
                )
                basket_item.save()
                items = BasketItem.objects.filter(basket=user_basket)
                serializer = BasketItemSerializer(items, many=True)
                return Response(serializer.data)


class AuthView(generics.GenericAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user),
            'auth': str(request.auth)
        }
        return Response(content)


class SearchProductListView(generics.GenericAPIView):
    serializer_class = ProductListSerializer
    queryset = Product.objects.all()

    def get(self, request, *args, **kwargs):
        q = self.request.GET.get('q')
        if q is not None:
            user = None
            if self.request.user.is_authenticated:
                user = self.request.user
            results = Product.objects.filter(name__contains=q)
            serializer = self.serializer_class(results, many=True)
        return Response(serializer.data)


class MyPurchasedProductsAPIView(generics.GenericAPIView):
    serializer_class = ProductPurchasedSerializer

    def get(self, request):
        if request.user:
            email = request.user
            user = CustomUser.objects.get(email=email)
            user_purchased_products = PurchasedProduct.objects.filter(user=user)
            serializer = self.serializer_class(user_purchased_products, many=True)
        return Response(serializer.data)


class CheckoutAPIView(generics.GenericAPIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.user:
            email = request.user
            user = CustomUser.objects.get(email=email)
            basket = Basket.objects.get(user=user)
            basket_items = BasketItem.objects.filter(basket=basket)
            for i in basket_items:
                purchased_product = PurchasedProduct.objects.get(product=i.product)
                if purchased_product:
                    purchased_product.quantity = purchased_product.quantity + i.quantity
                    purchased_product.save()
                else:
                    PurchasedProduct.objects.create(
                        user = user,
                        product = i.product,
                        quantity = i.quantity
                    )
                i.delete()
        return Response({})


class ProductRateAPIView(
    generics.GenericAPIView,
    mixins.CreateModelMixin
):
    serializer_class = RateSerializer

    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('productId')
        if product_id:
            rates = Rate.objects.filter(product=product_id)
            serializer = self.serializer_class(rates, many=True)
            return Response(serializer.data)
        return Response(status=400)


    def post(self, request, *args, **kwargs):
        self.serializer_class = RateAddSerializer
        author = CustomUser.objects.get(id=request.data['author'])
        product = Product.objects.get(id=request.data['product'])
        is_user_already_rated_product = Rate.objects.filter(author=author, product=product).exists()
        if is_user_already_rated_product:
            content = {'errors': ["You have already rated this product"]}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        return self.create(request, *args, **kwargs)


create_user_api_view = CreateUserAPIView.as_view()
user_by_token_api_view = CustomUserByTokenAPIView.as_view()
# user_api_view = GetUserAPIView.as_view()
product_api_view = ProductAPIView.as_view()
category_api_view = CategoryAPIView.as_view()
user_basket_api_view = BasketAPIView.as_view()
product_search_api_view = SearchProductListView.as_view()
my_purchased_products_api_view = MyPurchasedProductsAPIView.as_view()
checkout_api_view = CheckoutAPIView.as_view()
product_rate_api_view = ProductRateAPIView.as_view()
