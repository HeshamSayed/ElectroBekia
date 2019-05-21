from django.shortcuts import render
from orders.models import Order

def index(request):
  return render(request, 'base/home.html', {})

def get_extra_context():
  pass