from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _




class City(models.Model):
  name = models.CharField(max_length=50, blank=True, null=True)
  governorate = models.CharField(max_length=50, blank=True, null=True)
  status = models.BooleanField(default=0)

  def __str__(self):
    return self.name


class MyUserManager(BaseUserManager):
  """
  A custom user manager to deal with emails as unique identifiers for auth
  instead of usernames. The default that's used is "UserManager"
  """

  def _create_user(self, email, password, **extra_fields):
    """
    Creates and saves a User with the given email and password.
    """
    if not email:
      raise ValueError('The Email must be set')
    email = self.normalize_email(email)
    user = self.model(email=email, **extra_fields)
    user.set_password(password)
    user.save()
    return user

  def create_user(self, email, password=None, **extra_fields):
    """Create and save a regular User with the given email and password."""
    extra_fields.setdefault('is_staff', False)
    extra_fields.setdefault('is_superuser', False)
    return self._create_user(email, password, **extra_fields)

  def create_superuser(self, email, password, **extra_fields):
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)
    extra_fields.setdefault('is_active', True)

    if extra_fields.get('is_staff') is not True:
      raise ValueError('Superuser must have is_staff=True.')
    if extra_fields.get('is_superuser') is not True:
      raise ValueError('Superuser must have is_superuser=True.')

    return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    points = models.PositiveIntegerField(default=0)

    # 1 user 2 center
    user_category = models.BooleanField(default=1)

    phone_regex = RegexValidator(regex=r'^01[1|0|2|5][0-9]{8}$',
                                 message="Phone number must match egyptian format")
    phone = models.CharField(validators=[phone_regex], max_length=11,
                             blank=True, null=True,
                             help_text=_('من فضلك ادخل رقم موبايل صحيح'),)

    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)

    date_of_birth = models.DateField(blank=True, null=True)

    is_staff = models.BooleanField(
      _('staff status'),
      default=False,
      help_text=_('Designates whether the user can log into this site.'),
    )
    is_active = models.BooleanField(
      _('active'),
      default=True,
      help_text=_(
        'Designates whether this user should be treated as active. '
        'Unselect this instead of deleting accounts.'
      ),
    )

    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def __str__(self):
      return self.email

    def get_full_name(self):
      return self.email

    def get_short_name(self):
      return self.email


class PhoneNumber(models.Model):
  phone_regex = RegexValidator(regex=r'^01[1|0|2|5][0-9]{8}$',
                               message="Phone number must match egyptian format")
  phone = models.CharField(validators=[phone_regex], max_length=11,
                           blank=True, unique=True,
                           help_text=_('من فضلك ادخل رقم موبايل صحيح'))
  user = models.ForeignKey(User, on_delete=models.CASCADE)

