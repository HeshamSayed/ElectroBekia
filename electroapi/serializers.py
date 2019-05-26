from rest_framework import serializers
from products.models import Category, Product
from orders.models import Order


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "created_date")


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "category", "name", "description", "min_price", "max_price", "created_date", "updated_date", "image")

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "first_name", "last_name", "email", "phone", "address",
                  "city", "user", "created", "updated", "order_status", "get_total_cost")
