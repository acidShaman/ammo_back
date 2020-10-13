from django.contrib import admin

# Register your models here.
from menu.models import DishModel, MenuModel

admin.site.register(DishModel)
admin.site.register(MenuModel)
# admin.site.register(ImgModel)