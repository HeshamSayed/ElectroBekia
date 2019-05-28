from . import views
from django.urls import path

app_name = 'orders'

urlpatterns = [
  path('create/', views.order_create, name='order_create'),
  path('', views.order_list, name='order_list'),
  path('<int:pk>', views.order_detail, name='order_detail'),
  path('reply/<int:pk>', views.send_reply, name='send_reply'),
]
