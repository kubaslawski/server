from django.urls import path


from .views import user_api_view, product_api_view, category_api_view


urlpatterns = [
    path('users/', user_api_view),
    path('users/<int:pk>/', user_api_view),
    path('products/', product_api_view),
    path('products/<int:pk>/', product_api_view),
    path('products/category/<int:category_pk>/', product_api_view),
    path('categories/', category_api_view),
    path('categories/<int:pk>/', category_api_view),
]
