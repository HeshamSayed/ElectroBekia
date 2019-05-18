from django.shortcuts import render, get_object_or_404
from .models import *


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
  context = {
    'product': product,
  }

  return render(request, 'products/detail.html', context)
