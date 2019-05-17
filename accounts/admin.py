from django.contrib import admin
from .models import *


class UserAdmin(admin.ModelAdmin):
  list_display = ['first_name', 'last_name', 'email', 'points',
                  'user_category', 'city']
  list_filter = ['user_category']


admin.site.register(User, UserAdmin)
admin.site.register(City)
admin.site.register(PhoneNumber)
