from django import forms
from .models import Order
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from accounts.models import City


class OrderCreateForm(forms.ModelForm):
  first_name = forms.CharField(label='الاسم الاول', max_length=30, required=True)
  last_name = forms.CharField(label='الاسم الاخير', max_length=30, required=True)
  email = forms.EmailField(label='البريد الالكترونى', max_length=100, help_text='مطلوب', required=True)
  phone_regex = RegexValidator(
    regex=r'^01[1|0|2|5][0-9]{8}$',
    message="من فضلك ادخل رقم هاتف مصري صحيح"
  )
  phone = forms.CharField(
    label='رقم الهاتف المحمول',
    validators=[phone_regex], max_length=11, min_length=11,
    required=True, widget=forms.TextInput(attrs={
      'pattern': '^01[1|0|2|5][0-9]{8}$',
    }),
    help_text=_('من فضلك ادخل رقم موبايل صحيح')
  )
  address = forms.CharField(label='العنوان بالتفصيل', max_length=250, required=True)
  city = forms.ModelChoiceField(label='المدينه', queryset=City.objects, required=True)

  class Meta:
    model = Order
    fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'city']

class DeterminePriceForm(forms.Form):
  price = forms.FloatField(help_text="من فضلك أدخل رقم صحيح")
