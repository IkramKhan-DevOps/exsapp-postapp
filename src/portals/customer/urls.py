from django.urls import path
from .views import (
    DashboardView,
    UserListView, ParcelListView, SearchIDView, TestView, UserExistsJSON)

app_name = "customer"
urlpatterns = [

    path('', DashboardView.as_view(), name='dashboard'),
    path('user/', UserListView.as_view(), name='user'),
    path('parcel/', ParcelListView.as_view(), name='parcel'),
    path('parcel/search/', SearchIDView.as_view(), name='parcel-search'),
    path('add/parcel/', TestView.as_view(), name='add-parcel'),
    path('json/user/<str:username>/exists/', UserExistsJSON.as_view(), name='user-exists-json'),
]
