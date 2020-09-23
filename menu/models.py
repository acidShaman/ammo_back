import os

from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models

# Create your models here.


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
        RegexValidator('^([a-zA-Zа-яА-ЯєЄЇїёЁ ,./`!\']{1,50})$', 'Name can contain a-z A-Z and some spec chars max 50 chars')])
    category = models.ForeignKey(MenuModel, related_name='dishes', on_delete=models.CASCADE)
    price = models.PositiveIntegerField(blank=False)
    about_dish = models.CharField(max_length=300, blank=False, validators=[
        RegexValidator('^([a-zA-Zа-яА-ЯєЄЇїёЁ ,./`!\']{1,300})$', 'Info must contain letters and some spec chars max 300 chars')
    ])
    ingredients = models.CharField(max_length=300, blank=False, validators=[
        RegexValidator('^([a-zA-Zа-яА-ЯєЄЇїёЁ ,./`!\']{1,300})$', 'Info must contain letters and some spec chars max 300 chars')
    ])
    weight = models.PositiveIntegerField(blank=False, null=True)
    user_liked = models.ManyToManyField(User, through='FavoritesModel')

    def __str__(self):
        return ' ,'.join([str(self.id), str(self.name), str(self.category), str(self.price), str(self.about_dish), str(self.ingredients), str(self.weight)])


# class ImgModel(models.Model):
#     class Meta:
#         db_table = 'images'
#         verbose_name = 'image'
#         verbose_name_plural = 'images'
#
#     image = models.ImageField(upload_to=os.path.join('dishes', 'img'), default='', blank=True)
#     dish = models.ForeignKey(DishModel, on_delete=models.CASCADE)


# class IngredientModel(models.Model):
#     class Meta:
#         db_table = 'ingredients'
#         verbose_name = 'ingredient'
#         verbose_name_plural = 'ingredients'
#
#     ingredient = models.CharField(max_length=30, unique=True, validators=[
#         RegexValidator('^([a-zA-Z0-9.]{1,30})$', 'Ingredient might contain letters, numbers and . 30 chars maximum')])
#     dish = models.ManyToManyField(DishModel)


class FavoritesModel(models.Model):
    class Meta:
        db_table = 'favorite_dishes'
        verbose_name = 'fav_dish'
        verbose_name_plural = 'fav_dishes'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dish = models.ForeignKey(DishModel, on_delete=models.CASCADE)
