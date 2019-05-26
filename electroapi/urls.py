from django.urls import path
from .views import ListCategoryView, CategoryDetailView, ListProductView, ProductDetailView,\
    ListOrderView, OrderDetailView, LoginView
app_name = 'electroapi'

urlpatterns = [
    # /api/categories/ get all categories, post category
    path('categories/', ListCategoryView.as_view(), name="categories"),

    # /api/categories/id/ delete,update,get category
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name="category_details"),

    # /api/categories/id get all products, post product on category
    path('categories/<int:pk>/products/', ListProductView.as_view(), name="products"),

    # /api/categories/id/products/id delete,update,get product
    path('categories/<int:pk>/products/<int:id>/',ProductDetailView.as_view(), name="products_details"),

    # /api/orders/  get all orders, post order
    path('orders/', ListOrderView.as_view(), name="orders"),

    # /api/orders/id/ delete,update,get order
    path('orders/<int:pk>/', OrderDetailView.as_view(), name="category_details"),

    path('auth/login/', LoginView.as_view(), name="auth-login")
]