from django.contrib import admin

# Register your models here.
from menu.models import ImgModel, DishModel

admin.register(DishModel)
admin.register(ImgModel)