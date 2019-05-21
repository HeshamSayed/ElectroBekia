from django.contrib import admin
from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_date']
    list_per_page = 10
    class Media:
        css = {
            'all': ('css/admin/style.css',)
        }


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'min_price', 'max_price']
    list_per_page = 10
    fields = (('name', 'category'),
              ('min_price', 'max_price'),
              ('description'), ('image'))

    class Media:
        css = {
            'all': ('css/admin/style.css',)
        }


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
