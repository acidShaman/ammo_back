from django.contrib.auth.models import User
from django.core.validators import RegexValidator

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


class UserCreateSerializer(serializers.Serializer):
    username = serializers.EmailField(min_length=3, required=True)
    first_name = serializers.CharField(min_length=2, required=True)
    last_name = serializers.CharField(min_length=2, required=True)
    password = serializers.CharField(min_length=6, required=True,
                                     validators=[RegexValidator('^((?=\S*?[A-Z])(?=\S*?[a-z])(?=\S*?[0-9]).{6,})\S$',
                                                                'Password must contain minimum of 6 characters, at least 1 uppercase letter, 1 lowercase letter, and 1 number with no spaces.')])


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = ['sex', 'birthday', 'phone']
        extra_kwargs = {
            'sex': {
                'required': False
            },
            'birthday': {
                'required': False
            },
            'phone': {
                'required': False
            }
        }


class UserUpdateSerializer(serializers.ModelSerializer):
    profile = ProfileUpdateSerializer(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'profile']
        extra_kwargs = {
            'first_name': {
                'required': False
            },
            'last_name': {
                'required': False
            },
            'username': {
                'required': False
            }
        }


class AddressUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressModel
        fields = ['street', 'number', 'entrance', 'housing', 'door', 'floor']
        extra_kwargs = {
            'street': {
                'required': False
            },
            'number': {
                'required': False
            },
            'entrance': {
                'required': False
            },
            'housing': {
                'required': False
            },
            'door': {
                'required': False
            },
            'floor': {
                'required': False
            }
        }

    def update(self, instance, validated_data):
        instance.street = validated_data.get('street', '')
        instance.number = validated_data.get('number', '')
        instance.entrance = validated_data.get('entrance', '')
        instance.housing = validated_data.get('housing', '')
        instance.door = validated_data.get('door', '')
        instance.floor = validated_data.get('floor', '')
        instance.save()

        return instance














