from django.urls import path
from .views import ListCategoryView, CategoryDetailView, ListProductView, ProductDetailView,\
    ListOrderView, OrderDetailView, LoginView, RegisterUserView, ListOrderItemView, OrderItemDetailView
app_name = 'electroapi'

urlpatterns = [
    # /api/categories/ get all categories, post category
    path('categories/', ListCategoryView.as_view(), name="categories"),

    # /api/categories/id/ delete,update,get category
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name="category_details"),

    # /api/categories/id/products/ get all products, post product on category
    path('categories/<int:pk>/products/', ListProductView.as_view(), name="products"),

    # /api/categories/id/products/id delete,update,get product
    path('categories/<int:pk>/products/<int:id>/',ProductDetailView.as_view(), name="products_details"),

    # /api/orders/  get all orders, post order
    path('orders/', ListOrderView.as_view(), name="orders"),

    # /api/orders/id/ delete,update,get order
    path('orders/<int:pk>/', OrderDetailView.as_view(), name="category_details"),

    # /api/login/ to login user and recieve token
    path('login/', LoginView.as_view(), name="auth-login"),

    # /api/login/ to register user
    path('register/', RegisterUserView.as_view(), name="auth-register"),

    # /api/orders/id/items get all items, post item on order
    path('orders/<int:pk>/items/', ListOrderItemView.as_view(), name="items"),

    # /api/orders/id/items/id delete,update,get item
    path('orders/<int:pk>/items/<int:id>/',OrderItemDetailView.as_view(), name="order_details"),




]