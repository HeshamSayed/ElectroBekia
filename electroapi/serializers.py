from rest_framework import serializers
from products.models import Category, Product
from orders.models import Order
from accounts.models import User


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


class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email",)
