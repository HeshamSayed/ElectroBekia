from fnmatch import filter
from django import template
from django.contrib import admin
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import *
from django.db.models import Q , Count
from django.template.response import TemplateResponse
from django.urls import path
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
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
          path('new-orders/<int:id>/', self.admin_site.admin_view(self.view_new_order))
        ]
        return my_urls + urls
    def get_order_items_info(self , order_items):
      info = []
      for item in order_items : 
        info.append({
          "images" :[order_img.img.url for order_img in item.orderimage_set.all()] if item.orderimage_set else ["لا توجد صور"],
          "product" : item.product.name,
          "quantity" : item.quantity,
          "description" : item.description or "لا يوجد وصف"
        })
      return info
    def view_new_order (self , request , id,extra_context) :
      order = Order.objects.annotate(count=Count('items')).get(pk=id)
      order_items = OrderItem.objects.filter(order_id=id)
      paginator = Paginator(order_items, 3) # Show 9 orders per page
      page = request.GET.get('page')
      order_items = paginator.get_page(page)
      order_items_info = self.get_order_items_info(order_items)
      new_orders = Order.objects.filter(order_status = 1).count()
      user_type = "مستخدم عادي" if order.user.user_category else "مركز صيانة"
      print (user_type)
      context = {
        "user_type":user_type,
        "order":order,
        "count":order.count,
        "orders":order_items_info,
        "new_orders":new_orders,
        "page_ranges": reversed(range(1 , order_items.paginator.num_pages + 1)),
      }
      return render(request, 'orders/admin/new_order.html' ,context)




class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'price',
                    'quantity']
    list_filter = ['price']
    list_per_page = 10

    class Media:
        css = {
            'all': ('css/admin/style.css',)
        }


class OrderImageAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('css/admin/style.css',)
        }

def get_context(request, orders , order_type):
  orders_exists = True if orders else False
  paginator = Paginator(orders, 9) # Show 9 orders per page
  page = request.GET.get('page')
  orders_paged = paginator.get_page(page)
  orders_info = [(order,order.count) for order in orders_paged]
  new_orders = Order.objects.filter(order_status = 1).count()
  context= {
    "exists" : orders_exists,
    "orders" : orders_info,
    "page_ranges": reversed(range(1 , orders_paged.paginator.num_pages + 1)),
    "new_orders":new_orders,
    "order_type":order_type
  }
  return context
def new_orders(request,extra_context):
  orders = Order.objects.annotate(count=Count('items')).filter(order_status = 1)
  context = get_context(request, orders,"new-orders")
  return render(request, 'orders/admin/orders.html',context)
admin.site.register_view('new-orders/', view=new_orders)

def waiting_orders(request,extra_context):
  orders = Order.objects.annotate(count=Count('items')).filter(order_status = 2)
  context = get_context(request, orders,"waiting-orders")
  return render(request, 'orders/admin/orders.html',context)
admin.site.register_view('waiting-orders/', view=waiting_orders)

def old_orders(request,extra_context):
  orders = Order.objects.annotate(count=Count('items')).filter(order_status = 3)
  context = get_context(request, orders,"old-orders")
  return render(request, 'orders/admin/orders.html',context)
admin.site.register_view('old-orders/', view=old_orders)



admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(OrderImage,OrderImageAdmin)
