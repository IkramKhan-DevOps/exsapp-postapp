from django.urls import path
from src.api.views import UserUpdateView, UserImageView, ParcelViewSet, ReceiverParcelViewSet, UserParcelsView

app_name = 'api'

urlpatterns = [
    path('my/image/', UserImageView.as_view(), name="my-profile-image"),
    path('my/profile/', UserUpdateView.as_view(), name="my-profile-details"),
    path('parcel/<str:tracking_id>/', ParcelViewSet.as_view(), name="get-parcel-from-qr"),
    path('my/parcel/', UserParcelsView.as_view(), name="sender-postman-parcels"),
    path('receiver/parcel/', ReceiverParcelViewSet.as_view(), name="receiver-parcels"),
]
