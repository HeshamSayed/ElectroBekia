from django import template

register = template.Library()

@register.filter(name='to_ar')
def to_ar(value):
    devanagari_nums = ('۰', '۱', '۲', '۳', '٤', '۵', '٦', '۷', '۸', '۹')
    number = str(value)
    return ''.join(devanagari_nums[int(digit)] for digit in number)