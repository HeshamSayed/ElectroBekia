from fnmatch import filter
from django import template
from django.contrib import admin
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import *
from django.db.models import Q , Count
register = template.Library()



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

def new_orders(request):
  new_orders = Order.objects.annotate(count=Count('items')).filter(order_status = 1)
  orders_exists = True if new_orders else False
  paginator = Paginator(new_orders, 9) # Show 9 orders per page
  page = request.GET.get('page')
  orders = paginator.get_page(page)
  orders_info = [(order,order.count) for order in orders]
  context= {
    "exists" : orders_exists,
    "orders" : orders_info,
    "page_ranges": reversed(range(1 , orders.paginator.num_pages + 1)),
  }
  return render(request, 'orders/admin/orders.html',context)
admin.site.register_view('new-orders', view=new_orders)

def old_orders(request):
  old_orders = Order.objects.annotate(count=Count('items')).filter(~Q(order_status = 1))
  orders_exists = True if old_orders else False
  paginator = Paginator(old_orders, 9) # Show 9 orders per page
  page = request.GET.get('page')
  orders = paginator.get_page(page)
  orders_info = [(order,order.count) for order in orders]
  context= {
    "exists" : orders_exists,
    "orders" : orders_info,
    "page_ranges":reversed(range(1 , orders.paginator.num_pages + 1)),
  }
  return render(request, 'orders/admin/orders.html',context)
admin.site.register_view('old-orders', view=old_orders)



admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
