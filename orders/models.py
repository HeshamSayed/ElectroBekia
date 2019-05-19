from django.db import models
from products.models import Product
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from accounts.models import City, User
from django.core.validators import MaxValueValidator, MinValueValidator


class Order(models.Model):
  first_name = models.CharField(max_length=60, blank=True, null=True)
  last_name = models.CharField(max_length=60, blank=True, null=True)
  email = models.EmailField()
  phone_regex = RegexValidator(regex=r'^01[1|0|2|5][0-9]{8}$',
                               message="Phone number must match egyptian format")
  phone = models.CharField(validators=[phone_regex], max_length=11,
                           blank=True, null=True,
                           help_text=_('من فضلك ادخل رقم موبايل صحيح'))
  address = models.CharField(max_length=150, blank=True, null=True)

  city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  order_status = models.PositiveIntegerField(default=1)

  class Meta:
    ordering = ('-created',)

  def __str__(self):
    return "طلب " + self.first_name + " " + self.last_name

  def get_total_cost(self):
    return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
  order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
  product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
  price = models.FloatField(
    validators=[MinValueValidator(0.0), MaxValueValidator(1000000)],
  )
  quantity = models.PositiveIntegerField(default=1)

  def __str__(self):
    return self.product

  def get_cost(self):
    return self.price * self.quantity
