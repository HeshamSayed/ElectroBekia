"""ElectroBekia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include,re_path
from .view import *
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from adminplus.sites import AdminSitePlus
admin.site = AdminSitePlus()
admin.autodiscover()
urlpatterns = [
  path('', index, name='base'),
  path('admin/', admin.site.urls, {'extra_context': get_extra_context()}),
  path('accounts/', include('accounts.urls', namespace='accounts')),
  url(r'^oauth/', include('social_django.urls', namespace='social')),
  path('', index, name='base'),
  path('products/', include('products.urls', namespace='products')),
  path('cart/', include('cart.urls', namespace='cart')),
  path('orders/', include('orders.urls', namespace='orders')),
  path('api/', include('electroapi.urls', namespace='electroapi')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + staticfiles_urlpatterns()
