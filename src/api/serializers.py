from rest_framework import serializers
from src.accounts.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone_number',
        ]


class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'profile_image',
        ]