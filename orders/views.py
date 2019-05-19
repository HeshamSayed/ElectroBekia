from django.shortcuts import render, get_object_or_404
from .forms import OrderCreateForm
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from .models import *
from django.http import HttpResponse


@login_required
def order_create(request):
  cart = Cart(request)
  if request.method == 'POST':
    form = OrderCreateForm(request.POST)
    if form.is_valid():
      order = form.save(commit=False)
      order.user = request.user
      order.save()
      for item in cart:
        OrderItem.objects.create(
          order=order,
          product=item['product'],
          price=item['price'],
          quantity=item['quantity']
        )
      cart.clear()
    return HttpResponse('تم ارسال طلبك بنجاح برجاء الانتظار')
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

