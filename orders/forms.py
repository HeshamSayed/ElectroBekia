from django import forms
from .models import Order
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from accounts.models import City


class OrderCreateForm(forms.ModelForm):
  first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
    'class': "form-control input-lg text-right",
    'placeholder': "الاسم الاول",
    'autocomplete': 'off',
  }))
  last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
    'class': "form-control input-lg text-right",
    'placeholder': "الاسم الاخير",
    'autocomplete': 'off',
  }))
  email = forms.EmailField(max_length=100, required=True, widget=forms.EmailInput(attrs={
    'class': "form-control input-lg text-right",
    'placeholder': "البريد الالكترونى",
    'autocomplete': 'off',
  }))
  phone_regex = RegexValidator(
    regex=r'^01[1|0|2|5][0-9]{8}$',
    message="من فضلك ادخل رقم هاتف مصري صحيح"
  )
  phone = forms.CharField(
    validators=[phone_regex], max_length=11, min_length=11,
    required=True, widget=forms.TextInput(attrs={
      'pattern': '^01[1|0|2|5][0-9]{8}$',
      'placeholder': "رقم الهاتف المحمول",
      'class': "form-control input-lg text-right",
      'autocomplete': 'off',
    }),
    help_text=_('من فضلك ادخل رقم موبايل صحيح')
  )
  address = forms.CharField(max_length=250, required=True, widget=forms.Textarea(attrs={
    'class': "form-control input-lg text-right",
    'placeholder': "العنوان بالتفصيل",
    'name': "addre",
    'style': "resize: none;",
    'autocomplete': 'off',
    'rows': "2",
  }))
  city = forms.ModelChoiceField(
    queryset=City.objects, required=True, empty_label='المدينه',
    widget=forms.Select(attrs={
      'class': "form-control input-lg text-right",
      'autocomplete': 'off',
      'id': "sel1",
      'dir': 'rtl',
    }))
  Images = forms.ImageField(required=True, widget=forms.ClearableFileInput(attrs={
    'multiple': True,
    'class': "form-control input-lg text-right",
  }))
  description = forms.CharField(max_length=1250, required=True, widget=forms.Textarea(attrs={
    'class': "form-control input-lg text-right",
    'placeholder': "وصف منتجات الطلب",
    'style': "resize: none;",
    'autocomplete': 'off',
    'rows': "3",
  }))

  class Meta:
    model = Order
    fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'city', 'description']


class DeterminePriceForm(forms.Form):
  price = forms.FloatField(help_text="من فضلك أدخل رقم صحيح")
