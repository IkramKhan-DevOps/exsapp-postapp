from rest_framework import serializers
from src.accounts.models import User
from src.api.models import Parcel


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone_number', 'latitude', 'longitude', 'email', 'profile_image', 'is_postman',
            'is_customer', 'address'
        ]


class ParcelSerializer(serializers.ModelSerializer):
    receiver = UserProfileSerializer(many=False, read_only=True)
    sender = UserProfileSerializer(many=False, read_only=True)

    class Meta:
        model = Parcel
        fields = '__all__'


class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'profile_image',
        ]


