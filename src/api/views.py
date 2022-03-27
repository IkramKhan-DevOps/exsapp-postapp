import datetime

from rest_framework import generics, status
from rest_framework import permissions
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from src.accounts.models import User
from src.api.models import Parcel
from src.api.serializers import UserProfileSerializer, UserImageSerializer, ParcelSerializer


def get_api_exception(detail, code):
    api_exception = APIException()
    api_exception.status_code = code
    api_exception.detail = detail
    return api_exception


class UserUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ParcelViewSet(generics.RetrieveUpdateAPIView):
    queryset = Parcel.objects.all()
    serializer_class = ParcelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        print('TRACKING ID')
        print(self.kwargs.get('tracking_id'))
        parcel = Parcel.objects.get(tracking_id=self.kwargs.get('tracking_id'))
        parcel.status = 'pos'
        if self.request.user.is_postman:
            parcel.postman = self.request.user
            parcel.save()
        return parcel


class ParcelUpdateViewSet(APIView):
    serializer_class = ParcelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        print('TRACKING ID')
        print(self.kwargs.get('tracking_id'))
        parcel = Parcel.objects.get(tracking_id=self.kwargs.get('tracking_id'))
        message = "Parcel Deactivated"
        if self.request.user.is_postman:
            parcel.is_active = False
            parcel.expiry = datetime.datetime.now().replace(
                tzinfo=datetime.timezone(offset=datetime.timedelta())) + datetime.timedelta(hours=24)
            message = "Parcel Deactivated"
        if self.request.user.is_customer:
            print(parcel.expiry)
            print(datetime.datetime.now().replace(tzinfo=datetime.timezone(offset=datetime.timedelta())))
            if parcel.expiry > datetime.datetime.now().replace(tzinfo=datetime.timezone(offset=datetime.timedelta())):
                if parcel.is_active:
                    parcel.is_active = False
                    message = "Parcel status changed to \"Delivered\""
                else:
                    parcel.is_active = True
                    message = "Parcel status changed to \"Not Delivered\""
            else:
                message = "You cannot make changes in parcel, it is expired"
                Response(data={'message': message}, status=status.HTTP_406_NOT_ACCEPTABLE)
        print(message)
        parcel.save()
        return Response(data={'message': message}, status=status.HTTP_202_ACCEPTED)


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
            parcel = Parcel.objects.filter(customer=self.request.user)
        return parcel


class UserImageView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
