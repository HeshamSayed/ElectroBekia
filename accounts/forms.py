from django import forms
from django.contrib.auth.forms import UserCreationForm, get_user_model
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from .models import City


# <input type="text" class="form-control input-lg text-right"
#            placeholder="البريد الالكترونى" autocomplete='off'/>
#   </div>


class SignupForm(UserCreationForm):
  # error_messages = {
  # 'This password is too short. It must contain at least 8 characters.': "كلمه السر قصير يجب هلا تقل عن 8 احرف"
  # }
  first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
    'class': "form-control input-lg text-right",
    'placeholder': "الاسم الأول",
    'autocomplete': 'off',
  }))
  last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
    'class': "form-control input-lg text-right",
    'placeholder': "الاسم الأخير",
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
    help_text=_('من فضلك ادخل رقم هاتف صحيح'),
    
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
  }), help_text='الرقم السري يجب ان يكون على الأقل 8 حروف'
       )

  password2 = forms.CharField(widget=forms.PasswordInput(attrs={
    'placeholder': "تاكيد الرقم السرى",
    'class': "form-control input-lg text-right",
    'autocomplete': 'off',
  }), help_text='ادخل الرقم السري مرة أخرى للتاكيد')

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
  # boolfield = forms.ChoiceField(choices = TRUE_FALSE_CHOICES, label="Some Label", 
  #                               initial='', widget=forms.Select(), required=True)

  user_category = forms.ChoiceField(
    required=True,
    choices = USER_CATEGORIES,
    initial='نوع المستخدم',
    widget=forms.Select(attrs={
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
