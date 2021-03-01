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

    category = models.CharField(max_length=30, blank=False, unique=True, validators=[
        RegexValidator('^([a-zA-Z0-9 -]{1,20})$', 'Category must be only letters 1 - 20 chars long')])
    name = models.CharField(max_length=30, null=True, unique=True, validators=[
        RegexValidator("^([a-zA-ZА-Яа-яЇїєЄёЁіІ`'-.,0-9 ]{1,30})$")
    ])
    image = models.ImageField(upload_to=os.path.join('images', 'categories'), null=True, blank=True, default=None)
    isShown = models.BooleanField(default=False)

    def __str__(self):
        return ','.join([str(self.id), str(self.category)])


class DishModel(models.Model):
    class Meta:
        db_table = 'dishes'
        verbose_name = 'dish'
        verbose_name_plural = 'dishes'

    name = models.CharField(max_length=50, blank=False, unique=True, validators=[
        RegexValidator('^([0-9a-zA-Zа-яА-ЯєЄІіЇїёЁ+Ґґ\",./`: _!\']{1,50})$', 'Name can contain a-z A-Z and some spec chars max 50 chars')])
    category = models.ForeignKey(MenuModel, related_name='dishes', on_delete=models.CASCADE, blank=False)
    price = models.PositiveIntegerField(blank=False)
    about_dish = models.CharField(max_length=300, blank=False, validators=[
        RegexValidator('^([0-9a-zA-Zа-яА-ЯєЄЇїёЁІі+\"% ,-./`!\']{1,300})$', 'Info must contain letters and some spec chars max 300 chars')
    ])
    ingredients = models.CharField(max_length=300, blank=False, validators=[
        RegexValidator('^([0-9a-zA-Zа-яА-ЯєЄЇїёЁІі+\"% ,-./`!\']{1,300})$', 'Info must contain letters and some spec chars max 300 chars')
    ])
    image = models.ImageField(upload_to=os.path.join('images', 'dishes'), null=True, blank=True)
    weight = models.PositiveIntegerField(blank=False, null=True)


    def __str__(self):
        return ' ,'.join([str(self.id), str(self.name), str(self.category), str(self.price), str(self.about_dish), str(self.ingredients), str(self.weight)])

