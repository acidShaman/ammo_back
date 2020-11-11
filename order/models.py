from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from menu.models import DishModel
from profile.models import AddressModel, ProfileModel


class OrderItemModel(models.Model):
    class Meta:
        db_table = 'order_items'
        verbose_name = 'item'
        verbose_name_plural = 'items'

    dish = models.ForeignKey(DishModel, related_name='order_item',on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(blank=False)


class OrderModel(models.Model):
    class Meta:
        db_table = 'orders'
        verbose_name = 'order'
        verbose_name_plural = 'orders'

    profile = models.ForeignKey(ProfileModel, on_delete=models.CASCADE, null=True, related_name='order_history')
    address = models.ForeignKey(AddressModel, on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    order_items = models.ManyToManyField(OrderItemModel, related_name='orders')

