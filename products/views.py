from django.shortcuts import render, get_object_or_404
from .models import *
from cart.forms import CartAddProductForm


def product_list(request):
  categories = Category.objects.all()
  products = Product.objects.all()

  context = {
    'categories': categories,
    'products': products
  }

  return render(request, 'products/list.html', context)


def product_detail(request, pk):
  product = get_object_or_404(Product, pk=pk)
  cart_product_form = CartAddProductForm()

  context = {
    'product': product,
    'cart_product_form': cart_product_form,
  }

  return render(request, 'products/detail.html', context)
