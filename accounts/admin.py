from django.contrib import admin
from .models import *
from django.db.models import Value
from django.db.models.functions import Concat

admin.site.site_header = ' '


class UserAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'points',"password",
                    'city', 'User_Category', 'phone']
    list_display_links = [('full_name')]

    fieldsets = (
        (None, {
            'fields': (('first_name', 'last_name'),
                       ('phone', 'date_of_birth'),
                       ('is_active', 'city'),
                       ('is_staff', 'user_category'),
                       )
        }),
        ('read only', {
            # collasps to make input hidden and link show to show them
            'classes': ('collapse',),
            'fields': (('email'), ('points'), ('last_login')),
        }),
    )

    # filter()
    list_filter = ['user_category']
    list_per_page = 10
    search_fields = ['email']
    readonly_fields = ['last_login', 'points', 'email']
    view_on_site = False

    def has_add_permission(self, request, obj=None):
        return False

    def User_Category(self, obj):
        if obj.user_category == 1:
            return "مستخدم منزلي"
        else:
            return "مركز صيانة"

    def full_name(self, obj):
        if obj.first_name and obj.last_name:
            return obj.first_name + ' ' + obj.last_name
        elif obj.first_name:
            return obj.first_name
        elif obj.last_name:
            return obj.last_name
        else:
            return "has no name"
    change_list_template = 'admin/userlist.html'
    full_name.admin_order_field = Concat('first_name', Value(' '), 'last_name')
    full_name.short_description = "Full Name"
    User_Category.admin_order_field = 'user_category'

    empty_value_display = 'empty field'

    class Media:
        css = {
            'all': ('css/admin/style.css',)
        }

        js = ('js/admin/script.js',)


class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'governorate']

    class Media:
        css = {
            'all': ('css/admin/style.css',)
        }
        js = ('js/admin/script.js',)


class PhoneAdmin(admin.ModelAdmin):
    list_display = ['phone', 'user_name']

    # list_display_links = [('none')]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def user_name(self, obj):
        return obj.user.first_name + " " + obj.user.last_name

    user_name.admin_order_field = 'user'

    class Media:
        css = {
            'all': ('css/admin/style.css',)
        }


admin.site.register(User, UserAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(PhoneNumber, PhoneAdmin)
