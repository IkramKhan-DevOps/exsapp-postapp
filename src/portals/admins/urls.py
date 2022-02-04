from django.urls import path

from src.portals.admins.views import (
    DashboardView, UserListView, TestView,
    UserExistsJSON)

app_name = "admins"
urlpatterns = [

    path('', DashboardView.as_view(), name='dashboard'),
    path('user/', UserListView.as_view(), name='user'),
    path('add/parcel/', TestView.as_view(), name='add-parcel'),
    path('json/user/<str:username>/exists/', UserExistsJSON.as_view(), name='user-exists-json'),

]
