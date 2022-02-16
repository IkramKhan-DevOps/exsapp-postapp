import os
from src.accounts.permissions import PostmanCheck
from rest_framework import generics
from rest_framework import permissions

from src.accounts.models import User
from src.api.models import Parcel
from src.api.serializers import UserProfileSerializer, UserImageSerializer, ParcelSerializer


class UserUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ParcelViewSet(generics.RetrieveUpdateAPIView):
    queryset = Parcel.objects.all()
    serializer_class = ParcelSerializer
    permission_classes = [permissions.IsAuthenticated, PostmanCheck]

    def get_object(self):
        parcel = Parcel.objects.get(tracking_id=self.kwargs.get('tracking_id'))
        parcel.postman = self.request.user
        parcel.save()
        return parcel


class ReceiverParcelViewSet(generics.ListAPIView):
    queryset = Parcel.objects.all()
    serializer_class = ParcelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Parcel.objects.filter(receiver=self.request.user)


class UserParcelsView(generics.ListAPIView):
    queryset = Parcel.objects.all()
    serializer_class = ParcelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_postman:
            parcel = Parcel.objects.filter(postman=self.request.user)
        else:
            parcel = Parcel.objects.filter(sender=self.request.user)
        return parcel


class UserImageView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
