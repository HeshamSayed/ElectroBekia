from django import forms
from django.contrib.auth.forms import UserCreationForm, get_user_model
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from .models import City


class SignupForm(UserCreationForm):
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

    date_of_birth = forms.DateField(
      label='تاريخ الميلاد',
      widget=forms.DateInput(attrs={
        'type': 'date',
      }),
    )
    USER_CATEGORIES = [
      (1, '------------'),
      (1, 'مستخدم منزلى'),
      (0, 'ورشه تصليح'),
    ]
    user_category = forms.BooleanField(
      label='نوع المستخدم', required=True,
      widget=forms.Select(choices=USER_CATEGORIES)
    )
    password1 = forms.CharField(label='ادخل الرقم السري', widget=forms.PasswordInput,
                                help_text='الرقم السري يجب ان يكون على الاقل 8 حروف'
                                          ' من فضلك ادخل ارقام وحروف وعلامات مميزه')
    password2 = forms.CharField(label='تاكيد الرقم السرى', widget=forms.PasswordInput,
                                help_text='ادخل الرقم السري مره اخرى للتاكيد')

    city = forms.ModelChoiceField(label='المدينه', queryset=City.objects, required=True)

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'phone',
                  'password1', 'password2', 'date_of_birth',
                  'city', 'user_category')

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

