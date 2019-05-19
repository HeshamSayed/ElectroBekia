from django.contrib import admin
from .models import *


class OrderAdmin(admin.ModelAdmin):
  list_display = ['id', 'first_name', 'last_name', 'email',
                  'phone', 'city', 'order_status', 'user']
  list_filter = ['user']


class OrderItemAdmin(admin.ModelAdmin):
  list_display = ['id', 'order', 'product', 'price',
                  'quantity']
  list_filter = ['order__id']


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
