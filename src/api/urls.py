from django.urls import path
from src.api.views import UserUpdateView, UserImageView

app_name = 'api'

urlpatterns = [
    path('my/image/', UserImageView.as_view(), name="my-profile"),
    path('my/profile/', UserUpdateView.as_view(), name="my-profile-image"),
]
