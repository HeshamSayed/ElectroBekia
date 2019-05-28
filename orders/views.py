from curses.ascii import isdigit

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from cart.cart import Cart

from .forms import OrderCreateForm
from .models import *


@login_required
def order_create(request):
  cart = Cart(request)
  if request.method == 'POST':
    form = OrderCreateForm(request.POST)
    if form:
      order = Order()
      order.first_name = form['first_name'].value()
      order.last_name = form['last_name'].value()
      order.email = form['email'].value()
      order.phone = form['phone'].value()
      order.address = form['address'].value()
      order.city_id = int(form['city'].value())
      order.user = request.user
      order.save()
      for item in cart:
        OrderItem.objects.create(
          order=order,
          product=item['product'],
          price=item['price'],
          quantity=item['quantity']
        )
      if request.FILES['Images']:
        for i in request.FILES.getlist('Images'):
          picture = OrderImage(order=order, img=i)
          picture.save()
      cart.clear()
    return redirect('orders:order_detail', pk=order.id)
  else:
    form = OrderCreateForm()
    return render(request, 'orders/create.html', {'form': form})


def order_list(request):
  user_orders = Order.objects.filter(user=request.user)
  print(user_orders)
  context = {
    'orders': user_orders,
    'exists': True if user_orders else False
  }

  return render(request, 'orders/list.html', context)


def get_order_items_info(order_items):
    info = []
    for item in order_items:
        info.append({
            "product": item.product.name,
            "quantity": item.quantity,
            "id": item.id,
            "price": item.price or 0,
            "status":item.status
        })
    return info


def order_detail(request, pk):
  order = Order.objects.annotate(count=Count('items')).get(pk=pk)
  order_items = OrderItem.objects.filter(order_id=pk)
  paginator = Paginator(order_items, 10)  # Show 10 items per page
  page = request.GET.get('page')
  order_items = paginator.get_page(page)
  order_items_info = get_order_items_info(order_items)
  images = [order_img.img.url for order_img in order.orderimage_set.all()] if order.orderimage_set else ["لا توجد صور"],
  description=  order.description
  context = {
      "images":list(images)[0],
      "description":description or "لا يوجد وصف",
      "order": order,
      "count": order.count,
      "orders": order_items_info,
      "page_ranges": reversed(range(1, order_items.paginator.num_pages + 1)),
  }

  return render(request, 'orders/detail.html', context)

def send_reply(request, pk):
  print(dict(request.POST))
  for item_id , item_reply in dict(request.POST).items():
    print(item_id)
    if item_id.isdigit() :
        OrderItem.objects.filter(pk=item_id).update(status=item_reply[0])
  Order.objects.filter(pk=pk).update(order_status=3)
  return redirect('orders:order_detail', pk=pk)
