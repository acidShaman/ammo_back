from django.contrib.auth.models import User
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


    class Meta:
        model = ProfileModel
        fields = ['user', 'phone', 'birthday', 'sex']





