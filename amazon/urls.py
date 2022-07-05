from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from .views import  (
    product_api_view,
    category_api_view,
    user_by_token_api_view,
    user_basket_api_view,
    product_search_api_view,
    my_purchased_products_api_view,
checkout_api_view
)

urlpatterns = [
    # path('users/', user_api_view),
    # path('users/<int:pk>/', user_api_view),
    path('products/', product_api_view),
    path('products/<int:pk>/', product_api_view),
    path('products/category/<int:category_pk>/', product_api_view),
    path('categories/', category_api_view),
    path('categories/<int:pk>/', category_api_view),
    path('basket/', user_basket_api_view),
    path('search/products/', product_search_api_view),
    path('my-purchased-products/', my_purchased_products_api_view),
    path('checkout/', checkout_api_view),
    # authentication
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh_view'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify_view'),
    path('token/verify_user/', user_by_token_api_view)
]
