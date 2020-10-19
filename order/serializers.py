from django.contrib.auth.models import User

from menu.serializers import DishSerializer
from order.models import OrderModel, OrderItemModel
from profile.models import ProfileModel, AddressModel
from rest_framework import serializers


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressModel
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    address = AddressSerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'date_joined', 'address']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    fav_dishes = DishSerializer(read_only=True, many=True)

    class Meta:
        model = ProfileModel
        fields = ['user', 'phone', 'birthday', 'sex', 'fav_dishes']


class OrderItemSerializer(serializers.ModelSerializer):
    dish = DishSerializer()

    class Meta:
        model = OrderItemModel
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    address = AddressSerializer()
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = OrderModel
        fields = '__all__'
