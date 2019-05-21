from django import forms
from django.contrib.auth.forms import UserCreationForm, get_user_model
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from .models import City


# <input type="text" class="form-control input-lg text-right"
#            placeholder="البريد الالكترونى" autocomplete='off'/>
#   </div>


class SignupForm(UserCreationForm):
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
  email = forms.EmailField(max_length=100, help_text='مطلوب', required=True, widget=forms.EmailInput(attrs={
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

  date_of_birth = forms.DateField(
    label='تاريخ الميلاد',
    widget=forms.DateInput(attrs={
      'type': 'date',
    }),
  )

  password1 = forms.CharField(widget=forms.PasswordInput(attrs={
    'placeholder': "الرقم السرى",
    'class': "form-control input-lg text-right",
    'autocomplete': 'off',
  }), help_text='الرقم السري يجب ان يكون على الاقل 8 حروف'
                ' من فضلك ادخل ارقام وحروف وعلامات مميزه')

  password2 = forms.CharField(widget=forms.PasswordInput(attrs={
    'placeholder': "تاكيد الرقم السرى",
    'class': "form-control input-lg text-right",
    'autocomplete': 'off',
  }), help_text='ادخل الرقم السري مره اخرى للتاكيد')

  date_of_birth = forms.DateField(
    required=True, label='تاريخ الميلاد', widget=forms.DateInput(attrs={
      'class': "form-control input-lg text-right",
      'autocomplete': 'off',
      'type': 'date',
    }))

  city = forms.ModelChoiceField(
    queryset=City.objects, required=True, empty_label='البلد',
    widget=forms.Select(attrs={
      'class': "form-control input-lg text-right",
      'autocomplete': 'off',
      'id': "sel1",
      'dir': 'rtl',
    }))

  USER_CATEGORIES = [
    ('', 'نوع المستخدم'),
    (1, 'مستخدم منزلى'),
    (0, 'مركز صيانه'),
  ]

  user_category = forms.BooleanField(
    required=True,
    widget=forms.Select(choices=USER_CATEGORIES, attrs={
      'class': "form-control input-lg text-right",
      'autocomplete': 'off',
      'id': "sel1",
      'dir': 'rtl',
    })
  )

  class Meta:
    model = get_user_model()
    fields = ('first_name', 'last_name', 'email', 'phone',
              'password1', 'password2', 'date_of_birth',
              'city', 'user_category')

    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
