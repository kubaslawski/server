from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import user_api_view, product_api_view, category_api_view


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
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh_view')

    # path('auth/', auth_api_view),
    # path('api-token-auth/', auth_views.obtain_auth_token),

]
