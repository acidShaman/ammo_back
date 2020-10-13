import os
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

from menu.models import DishModel


class ProfileModel(models.Model):
    class Meta:
        db_table = 'profiles'
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'

    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=False, unique=True, validators=[
        RegexValidator('^\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$',
                       'Phone number must look like this +380112233445')],
                             error_messages={'error': 'Phone number might already ne used, please try another one'})
    birthday = models.DateField(max_length=10)
    sex = models.CharField(max_length=10, default='not given')
    fav_dishes = models.ManyToManyField(DishModel, related_name='favorited_by')

    def __str__(self):
        return f'{self.user.username}, {self.user.first_name}, {self.user.last_name}, {self.sex}, {self.birthday}, {self.phone}'


class AddressModel(models.Model):
    class Meta:
        db_table = 'addresses'
        verbose_name = 'address'
        verbose_name_plural = 'addresses'

    user = models.ForeignKey(User, related_name='address', on_delete=models.CASCADE)
    street = models.CharField(max_length=50, blank=False, validators=[
        RegexValidator('^([a-zA-Zа-яА-ЯЄєЇїёЁ.,-]{1,50})$', 'Street must contain only letters and , . -')])
    number = models.CharField(max_length=6, blank=False, validators=[
        RegexValidator('^([0-9]+\s*([a-zA-ZА-Яа-я]{0,}))$', 'Number must look like 78a or 78')])
    entrance = models.CharField(max_length=6, blank=True, null=True, validators=[
        RegexValidator('^([0-9]+\s*([a-zA-ZА-Яа-я]{0,}))$', 'Number must look like 78a or 78')])
    housing = models.CharField(max_length=5, blank=True, null=True, validators=[
        RegexValidator('^([0-9]+\s*([a-zA-ZА-Яа-я]{0,}))$', 'Number must look like 78a or 78')])
    door = models.CharField(max_length=7, blank=True, null=True, validators=[
        RegexValidator('^([0-9]+\s*([a-zA-Zа-яА-Я]{0,}))$', 'Number must look like 78a or 78')])
    floor = models.CharField(max_length=6, blank=True, null=True, validators=[
        RegexValidator('^([0-9]{0,}))$', 'Number must look like 78a or 78')])


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




