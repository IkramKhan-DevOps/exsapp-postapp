from django.urls import path

from src.portals.admins.views import (
    DashboardView, UserListView
)

app_name = "admins"
urlpatterns = [

    path('', DashboardView.as_view(), name='dashboard'),
    path('user/', UserListView.as_view(), name='user'),

]
