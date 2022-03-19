from django.urls import path

from src.portals.admins.views import (
    DashboardView, UserListView, TestView, ParcelListView,
    UserExistsJSON, SearchIDView, AddUserView, AddSuperUserView,
    )

app_name = "admins"
urlpatterns = [

    path('', DashboardView.as_view(), name='dashboard'),
    path('user/', UserListView.as_view(), name='user'),
    path('parcel/', ParcelListView.as_view(), name='parcel'),
    path('parcel/search/', SearchIDView.as_view(), name='parcel-search'),
    path('add/parcel/', TestView.as_view(), name='add-parcel'),
    path('json/user/<str:username>/exists/', UserExistsJSON.as_view(), name='user-exists-json'),

    path('add/user/', AddUserView.as_view(), name='add-user'),
    path('add/admin/user/', AddSuperUserView.as_view(), name='add-super-user'),
]
