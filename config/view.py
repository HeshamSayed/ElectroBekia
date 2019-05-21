from django.shortcuts import render
from orders.models import Order
from accounts.models import User


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