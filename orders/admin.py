from django.contrib import admin
from .models import *


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'phone', 'city', 'order_status', 'user']
    list_filter = ['user']
    list_per_page = 10

    class Media:
        css = {
            'all': ('css/admin/style.css',)
        }


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'price',
                    'quantity']
    list_filter = ['price']
    list_per_page = 10

    class Media:
        css = {
            'all': ('css/admin/style.css',)
        }


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
