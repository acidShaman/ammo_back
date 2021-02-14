from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


from menu.models import DishModel


class ProfileModel(models.Model):
    class Meta:
        db_table = 'profiles'
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'

    user = models.OneToOneField(User, related_name='profile', blank=True,on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=False, unique=True, validators=[
        RegexValidator('^\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$',
                       'Phone number must look like this +380112233445')],
                             error_messages={'error': 'Phone number might already ne used, please try another one'})
    birthday = models.DateField(max_length=10, null=True)
    sex = models.CharField(max_length=10, default='not given')
    fav_dishes = models.ManyToManyField(DishModel, related_name='favorited_by')

    # order_history = models.ManyToManyField(OrderModel, related_name='ordered_by')

    def __str__(self):
        return f'{self.user.username}, {self.user.first_name}, {self.user.last_name}, {self.sex}, {self.birthday}, {self.phone}'


class AddressModel(models.Model):
    class Meta:
        db_table = 'addresses'
        verbose_name = 'address'
        verbose_name_plural = 'addresses'

    profile = models.ForeignKey(ProfileModel, related_name='address',
                                on_delete=models.CASCADE, null=True)
    street = models.CharField(max_length=50, blank=False, validators=[
        RegexValidator('^([a-zA-Zа-яА-ЯЄєЇїёЁ.,-]{1,50})$', 'Street must contain only letters and , . -')])
    number = models.CharField(max_length=6, blank=False, validators=[
        RegexValidator('^([0-9]+\s*([a-zA-ZА-Яа-яЄєЇїёЁ.,-]{0,}))$', 'Number must look like 78a or 78')])
    entrance = models.CharField(max_length=6, blank=True, null=True, validators=[
        RegexValidator('^([0-9]+\s*([a-zA-ZА-Яа-яЄєЇїёЁ.,-]{0,}))$', 'Number must look like 78a or 78')])
    housing = models.CharField(max_length=5, blank=True, null=True, validators=[
        RegexValidator('^([0-9]+\s*([a-zA-ZА-Яа-яЄєЇїёЁ.,-]{0,}))$', 'Number must look like 78a or 78')])
    door = models.CharField(max_length=7, blank=True, null=True, validators=[
        RegexValidator('^([0-9]+\s*([a-zA-Zа-яА-ЯЄєЇїёЁ.,-]{0,}))$', 'Number must look like 78a or 78')])
    floor = models.CharField(max_length=6, blank=True, null=True, validators=[
        RegexValidator('^([0-9]{0,})$', 'Number must look like 78a or 78')])

    def __str__(self):
        return f'{self.user.username}-- {self.street} #{self.number}'



