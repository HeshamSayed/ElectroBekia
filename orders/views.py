from django.shortcuts import render, get_object_or_404, redirect
from .forms import OrderCreateForm
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
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

  context = {
    'oredrs': user_orders
  }

  return render(request, 'orders/list.html', context)


def order_detail(request, pk):
  order = get_object_or_404(Order, pk=pk)

  context = {
    'order': order,
  }

  for item in order.items.all():
    print(item.product)

  return render(request, 'orders/detail.html', context)