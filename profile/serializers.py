from django.contrib.auth.models import User

from menu.serializers import DishSerializer
from order.serializers import OrderSerializer
from profile.models import ProfileModel, AddressModel
from rest_framework import serializers


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressModel
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'date_joined']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    fav_dishes = DishSerializer(read_only=True, many=True)
    order_history = OrderSerializer(many=True)
    address = AddressSerializer(many=True)

    class Meta:
        model = ProfileModel
        fields = ['user', 'phone', 'birthday', 'sex', 'fav_dishes', 'order_history', 'address']