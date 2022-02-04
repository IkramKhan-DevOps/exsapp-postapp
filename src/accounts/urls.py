from django.urls import path

from .views import CrossAuthView, UserUpdateView

app_name = 'accounts'
urlpatterns = [
    path('cross-auth/', CrossAuthView.as_view(), name='cross-auth-view'),
    path('user/change/', UserUpdateView.as_view(), name='user-change'),
]
