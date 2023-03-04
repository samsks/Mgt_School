from rest_framework.views import Request, View
from schools.models import School
from rest_framework import permissions


class IsAdminOrSchoolOwner(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: School):
        return request.user.is_superuser or request.user == obj.account
