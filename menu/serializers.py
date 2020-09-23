from django.contrib.auth.models import User

from menu.models import MenuModel, DishModel
from profile.models import ProfileModel, AddressModel
from rest_framework import serializers


# class AddressSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AddressModel
#         fields = '__all__'
#
#
# class UserSerializer(serializers.ModelSerializer):
#     address = AddressSerializer(many=True)
#
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'first_name', 'last_name', 'date_joined', 'address']
#
#
# class ProfileSerializer(serializers.ModelSerializer):
#     user = UserSerializer()
#
#
#     class Meta:
#         model = ProfileModel
#         fields = ['user', 'phone', 'birthday', 'sex']

# class ImgSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ImgModel
#         fields = '__all__'


# class IngredientSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = IngredientModel
#         fields = '__all__'


class DishSerializer(serializers.ModelSerializer):
    # ingredients = IngredientSerializer(many=True)
    # images = ImgSerializer(many=True)

    class Meta:
        model = DishModel
        fields = ['id', 'name', 'price', 'about_dish', 'ingredients']


class MenuSerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True)

    class Meta:
        model = MenuModel
        fields = ['id', 'category', 'dishes']













