from rest_framework import serializers
from products.models import Category, Product
from orders.models import Order, OrderItem , OrderImage
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
                  "city", "user", "created", "updated", "order_status", "description")


class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email","first_name","last_name","user_category","phone","city","date_of_birth")


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ("id", "order","product","price","quantity","status")

class OrderImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderImage
        fields = ("id", "order", "img")

