import os
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


class MenuModel(models.Model):
    class Meta:
        db_table = 'menu'
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    category = models.CharField(max_length=20, blank=False,unique=True, validators=[
        RegexValidator('^([a-zA-Z]{1,20})$', 'Category must be only letters 1 - 20 chars long')])


class DishModel(models.Model):
    class Meta:
        db_table = 'dishes'
        verbose_name = 'dish'
        verbose_name_plural = 'dishes'

    name = models.CharField(max_length=50, blank=False, unique=True, validators=[
        RegexValidator('^([a-zA-Z,./`!\']{1,50})$', 'Name can contain a-z A-Z and some spec chars max 50 chars')])
    category = models.ForeignKey(MenuModel, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(blank=False)
    user_liked = models.ManyToManyField(User, through='FavoritesModel')


class ImgModel(models.Model):
    class Meta:
        db_table = 'images'
        verbose_name = 'image'
        verbose_name_plural = 'images'

    image = models.ImageField(upload_to=os.path.join('dishes', 'img'), default='', blank=True)
    dish = models.ForeignKey(DishModel, on_delete=models.CASCADE)


class IngredientModel(models.Model):
    class Meta:
        db_table = 'ingredients'
        verbose_name = 'ingredient'
        verbose_name_plural = 'ingredients'

    ingredient = models.CharField(max_length=30, unique=True, validators=[
        RegexValidator('^([a-zA-Z0-9.]{1,30})$', 'Ingredient might contain letters, numbers and . 30 chars maximum')])
    dish = models.ManyToManyField(DishModel)


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

    def __str__(self):
        return f'{self.user.username}, {self.user.first_name}, {self.user.last_name}, {self.sex}, {self.birthday}, {self.phone}'


class AddressModel(models.Model):
    class Meta:
        db_table = 'addresses'
        verbose_name = 'address'
        verbose_name_plural = 'addresses'

    user = models.ForeignKey(User, related_name='addresses', on_delete=models.CASCADE)
    street = models.CharField(max_length=50, blank=False, validators=[
        RegexValidator('^([a-zA-Z.,-]{1,50})$', 'Street must contain only letters and , . -')])
    number = models.CharField(max_length=6, blank=False, validators=[
        RegexValidator('^([0-9]+\s*([a-zA-ZА-Яа-я]{0,}))$', 'Number must look like 78a or 78')])
    entrance = models.IntegerField(blank=True, null=True)
    housing = models.CharField(max_length=5, blank=True, null=True)
    door = models.CharField(max_length=7, blank=True, null=True,validators=[
        RegexValidator('^([0-9]+\s*([a-zA-Z]{0,}))$', 'Number must look like 78a or 78')])
    floor = models.IntegerField(blank=True, null=True)


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


class FavoritesModel(models.Model):
    class Meta:
        db_table = 'favorite_dishes'
        verbose_name = 'fav_dish'
        verbose_name_plural = 'fav_dishes'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dish = models.ForeignKey(DishModel, on_delete=models.CASCADE)
