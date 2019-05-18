from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Category(models.Model):
  name = models.CharField(max_length=150, db_index=True, blank=True, null=True)
  created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

  class Meta:
    ordering = ('name', )

  def __str__(self):
    return self.name


class Product(models.Model):
  category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
  name = models.CharField(max_length=100, db_index=True, blank=True, null=True)
  description = models.TextField(blank=True)
  min_price = models.PositiveIntegerField()
  min_price = models.FloatField(
    validators=[MinValueValidator(0.0), MaxValueValidator(1000)],
  )
  max_price = models.FloatField(
    validators=[MinValueValidator(0.0), MaxValueValidator(100000)],
  )
  created_date = models.DateTimeField(auto_now_add=True)
  updated_date = models.DateTimeField(auto_now=True)
  image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)

  class Meta:
    ordering = ('created_date', )

  def __str__(self):
    return self.name

