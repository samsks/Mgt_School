from rest_framework.views import Request, View
from accounts.models import Account
from rest_framework import permissions


class IsAccountOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: Account):
        return request.user == obj or request.user.is_superuser


class IsAccountRoleOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        return request.user.role == "Owner" or request.user.is_superuser


class IsAccountHasSchool(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        return request.user.school_id is not None


class IsAuthenticatedAndAdmin(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: Account):
        return request.user.is_superuser and request.user.is_authenticated
