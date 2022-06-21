from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from .views import  product_api_view, category_api_view, user_api_view, user_by_token_api_view


urlpatterns = [
    path('users/', user_api_view),
    path('users/<int:pk>/', user_api_view),
    path('products/', product_api_view),
    path('products/<int:pk>/', product_api_view),
    path('products/category/<int:category_pk>/', product_api_view),
    path('categories/', category_api_view),
    path('categories/<int:pk>/', category_api_view),
    # authentication
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh_view'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify_view'),
    path('token/verify_user/', user_by_token_api_view)
]
