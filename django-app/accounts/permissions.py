from rest_framework.views import Request, View
from accounts.models import Account
from rest_framework import permissions


class IsAccountOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: Account):
        return request.user == obj or request.user.is_superuser


class IsAuthenticatedAndAdmin(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: Account):
        return request.user.is_superuser and request.user.is_authenticated
