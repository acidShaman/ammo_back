from django.contrib.auth.models import User

from menu.serializers import DishSerializer
from order.models import OrderModel, OrderItemModel
from rest_framework import serializers

from profile.models import AddressModel


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressModel
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    dish = DishSerializer()

    class Meta:
        model = OrderItemModel
        fields = ['id', 'quantity', 'dish']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = OrderModel
        fields = ['id', 'created', 'order_items']
