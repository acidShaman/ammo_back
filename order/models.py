from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from menu.models import DishModel
from profile.models import AddressModel


class OrderItemModel(models.Model):
    class Meta:
        db_table = 'order_items'
        verbose_name = 'item'
        verbose_name_plural = 'items'

    dish = models.ForeignKey(DishModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(blank=False)


class OrderModel(models.Model):
    class Meta:
        db_table = 'orders'
        verbose_name = 'order'
        verbose_name_plural = 'orders'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(AddressModel, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)
    order_items = models.ManyToManyField(OrderItemModel, related_name='orders')
