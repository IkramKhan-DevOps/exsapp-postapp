from rest_framework import permissions


class PostmanCheck(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return request.user.type == 'Postman'

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        return request.user.type == 'Postman'
