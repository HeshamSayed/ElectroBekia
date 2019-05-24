from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from accounts.models import User
from orders.models import Order
from django.contrib import admin
from orders.models import *
from django.core.paginator import Paginator
from django.db.models import  Count


def index(request):
  return render(request, 'base/home.html', {})

def get_extra_context():
  # all users including admin
  total_users = User.objects.count()
  new_orders = Order.objects.filter(order_status = 1).count()
  old_orders = Order.objects.filter(order_status = 3).count()
  waiting_orders = Order.objects.filter(order_status = 2).count()
  all_orders = Order.objects.count()
  context = {
    "total_users" : total_users ,
    "new_orders": new_orders,
    "old_orders" : old_orders,
    "waiting_orders" : waiting_orders,
    "all_orders" : all_orders
  }
  return context
def get_context(request, orders):
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
    "new_orders":new_orders
  }
  return context
