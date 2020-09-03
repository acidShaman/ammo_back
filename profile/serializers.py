from profile.models import ProfileModel
from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = ['user', 'phone', 'birthday', 'sex']

