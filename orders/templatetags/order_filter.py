from django import template
from accounts.models import User
from orders.models import *
register = template.Library()


@register.filter(name='to_ar')
def to_ar(value):
    print("value to ar")
    devanagari_nums = (	u"\u0660", 	u"\u0661", 	u"\u0662", 	u"\u0663",
                        u"\u0664",	u"\u0665",	u"\u0666", 	u"\u0667", 	u"\u0668", u"\u0669")
    parts = str(value).split('.')
    number = str(parts[0])
    if len(parts) == 1:
        ar_nm = ''.join(devanagari_nums[int(digit)] for digit in number)
    else:
        dec = str(parts[1])
        ar_nm = ''.join(devanagari_nums[int(digit)] for digit in number) + \
            ','+''.join(devanagari_nums[int(digit)] for digit in dec)
    return ar_nm


@register.filter(name='get_data')
def get_data(value):
    # all users including
    data = {
        "total_users": User.objects.count(),
        "new_orders": Order.objects.filter(order_status=1).count(),
        "waiting_orders": Order.objects.filter(order_status=2).count(),
        "old_orders": Order.objects.filter(order_status=3).count(),
        "done_orders": Order.objects.filter(order_status=4).count(),
        "all_orders": Order.objects.count()}
    return data[value]
