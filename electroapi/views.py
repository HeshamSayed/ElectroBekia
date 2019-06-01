from django.shortcuts import render

# Create your views here.

#Category Api
from .Category import ListCategoryView, CategoryDetailView

from .Product import ListProductView, ProductDetailView

from .Order import ListOrderView, OrderDetailView

from .Login import LoginView

from .Register import RegisterUserView

from .OrderItem import ListOrderItemView, OrderItemDetailView