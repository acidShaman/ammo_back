from django.contrib.auth.models import User

from menu.models import MenuModel, DishModel
from rest_framework import serializers




# class ImgSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ImgModel
#         fields = ['image']


# class IngredientSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = IngredientModel
#         fields = '__all__'
from profile.models import ProfileModel


class DishSerializer(serializers.ModelSerializer):
    # ingredients = IngredientSerializer(many=True)
    # images = ImgSerializer(many=True)

    class Meta:
        model = DishModel
        fields = ['id', 'name', 'price', 'about_dish', 'ingredients', 'image']


class MenuSerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True)

    class Meta:
        model = MenuModel
        fields = ['id', 'category', 'name', 'dishes']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuModel
        fields = ['id', 'category', 'name', 'image']














