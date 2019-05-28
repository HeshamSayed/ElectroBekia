from fnmatch import filter
from os import replace

from django import template
from django.contrib import admin
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import redirect, render
from django.template.response import TemplateResponse
from django.urls import path

from .forms import DeterminePriceForm
from .models import *

register = template.Library()


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
            path('done-orders/<int:id>/',
                 self.admin_site.admin_view(self.view_done_order)),
            path('old-orders/<int:id>/',
                 self.admin_site.admin_view(self.view_old_order)),
            path('old-orders/<int:id>/mark_done/',
                 self.admin_site.admin_view(self.mark_done), name="mark_done"),
            path('waiting-orders/<int:id>/',
                 self.admin_site.admin_view(self.view_waiting_order)),
            path('waiting-orders/<int:id>/change_price/',
                 self.admin_site.admin_view(self.change_price), name="change_price"),
            path('new-orders/<int:id>/',
                 self.admin_site.admin_view(self.view_new_order)),
            path('new-orders/<int:id>/update_price/',
                 self.admin_site.admin_view(self.update_price), name="update_price"),
            path('new-orders/<int:id>/send_price/',
                 self.admin_site.admin_view(self.send_price), name="send_price"),
        ]
        return my_urls + urls

    def get_order_items_info(self, order_items):
        info = []
        for item in order_items:
            status = item.status
            if status =='r' :
                item_status = 0
            elif status == 'a' :
                item_status = 1
            else : 
                item_status = -1
            info.append({
                "product": item.product.name,
                "quantity": item.quantity,
                "id": item.id,
                "price": item.price or 0,
                "status": item_status
            })
        return info

    def get_order_info(self, request, order_id):
        order = Order.objects.annotate(count=Count('items')).get(pk=order_id)
        order_items = OrderItem.objects.filter(order_id=order_id)
        paginator = Paginator(order_items, 10)  # Show 10 items per page
        page = request.GET.get('page')
        order_items = paginator.get_page(page)
        order_items_info = self.get_order_items_info(order_items)
        user_type = "مستخدم عادي" if order.user.user_category else "مركز صيانة"
        images = [order_img.img.url for order_img in order.orderimage_set.all()] if order.orderimage_set else ["لا توجد صور"],
        description=order.description
        return {
            "images":list(images)[0],
            "description":description or "لا يوجد وصف",
            "user_type": user_type,
            "order": order,
            "count": order.count,
            "orders": order_items_info,
            "page_ranges": reversed(range(1, order_items.paginator.num_pages + 1)),
        }

    def view_new_order(self, request, id):
        item = request.GET.get('item', '')  # get error some items has no price
        err = ''
        if item:
            err = "من فضلك أدخل أسعار الأصناف التالية : " + \
                item.replace('/', '')[:-2]
        form = DeterminePriceForm()
        order_info = self.get_order_info(request, id)
        new_order_info = {
            "err": err,
            'form': form,
        }
        context = {** new_order_info, ** order_info}
        return render(request, 'orders/admin/new_order.html', context)

    def update_price(self, request, id):
        order_id = request.POST['order_id']
        OrderItem.objects.filter(pk=id).update(price=request.POST['price'])
        return redirect('/admin/orders/order/new-orders/'+str(order_id)+'/')

    def send_price(self, request, id):
        finished_order = Order.objects.filter(pk=id)
        items = OrderItem.objects.filter(order_id=id)
        missed_item = ''
        for item in items:
            if item.price == 0.0 or not item.price:
                missed_item += "  "+str(item.product) + " - "
        if missed_item:
            return redirect('/admin/orders/order/new-orders/'+str(id)+'?item='+missed_item+'/')
        else:
            finished_order.update(order_status=2)
            return redirect('/admin/orders/order/waiting-orders/'+str(id)+'/')

      # Waiting order Actions
    def view_waiting_order(self, request, id):
        context = {**self.get_order_info(request, id), **{"order_type": 'waiting'}}
        return render(request, 'orders/admin/old_order.html', context)

    def change_price(self, request, id):
        Order.objects.filter(pk=id).update(order_status=1)
        return redirect('/admin/orders/order/new-orders/'+str(id)+'/')

      # Confirmed orders Actions
    def view_old_order(self, request, id):
        context = {**self.get_order_info(request, id), **{"order_type": 'old'}}
        return render(request, 'orders/admin/old_order.html', context)

    def mark_done(self, request, id):
        Order.objects.filter(pk=id).update(order_status=4)
        return redirect('/admin/orders/order/done-orders/'+str(id)+'/')
    def view_done_order(self, request, id):
        context = {**self.get_order_info(request, id), **{"order_type": 'done'}}
        return render(request, 'orders/admin/old_order.html', context)


# Admin tabs


def get_context(request, orders, order_type):
    orders_exists = True if orders else False
    paginator = Paginator(orders, 9)  # Show 9 orders per page
    page = request.GET.get('page')
    orders_paged = paginator.get_page(page)
    orders_info = [(order, order.count) for order in orders_paged]
    context = {
        "exists": orders_exists,
        "orders": orders_info,
        "page_ranges": reversed(range(1, orders_paged.paginator.num_pages + 1)),
        "order_type": order_type
    }
    return context


def new_orders(request):
    orders = Order.objects.annotate(
        count=Count('items')).filter(order_status=1)
    context = get_context(request, orders, "new-orders")
    return render(request, 'orders/admin/orders.html', context)


admin.site.register_view('new-orders/', view=new_orders)


def waiting_orders(request):
    orders = Order.objects.annotate(
        count=Count('items')).filter(order_status=2)
    context = get_context(request, orders, "waiting-orders")
    return render(request, 'orders/admin/orders.html', context)


admin.site.register_view('waiting-orders/', view=waiting_orders)


def old_orders(request):
    orders = Order.objects.annotate(
        count=Count('items')).filter(order_status=3)
    context = get_context(request, orders, "old-orders")
    return render(request, 'orders/admin/orders.html', context)
admin.site.register_view('old-orders/', view=old_orders)

def done_orders(request):
    orders = Order.objects.annotate(
        count=Count('items')).filter(order_status=4)
    context = get_context(request, orders, "done-orders")
    return render(request, 'orders/admin/orders.html', context)


admin.site.register_view('done-orders/', view=done_orders)


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(OrderImage, OrderImageAdmin)
