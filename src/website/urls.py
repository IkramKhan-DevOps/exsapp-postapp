from django.urls import path
from .views import (
    HomeView, Error404View, PrivacyPolicyView, TermsAndConditionsView
)

app_name = "website"

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy-policy'),
    path('terms-and-conditions/', TermsAndConditionsView.as_view(), name='terms-and-conditions'),
    path('404/', Error404View.as_view(), name='404'),
]