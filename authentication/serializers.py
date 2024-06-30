from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        CustomUser = CustomUser.objects.create_CustomUser(**validated_data)
        return CustomUser
