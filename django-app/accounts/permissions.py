from rest_framework.views import Request, View
from accounts.models import Account, ClassRegistration, TestResult, Attendance
from rest_framework import permissions
from schools.models import School
from courses.models import Course
from classes.models import Class
from classrooms.models import Classroom
from ttests.models import Test
from occurrences.models import Occurrence


class IsAccountOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: Account):
        return request.user == obj or request.user.is_superuser


class IsAccountRoleOwner(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        if request.user.role == "Owner":
            return True
        return False


class IsAccountRoleOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        return request.user.role == "Owner" or request.user.is_superuser


class IsAccountRoleTeacherOrAdmin(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        return request.user.role == "Teacher" or request.user.is_superuser


class IsAccountRoleOwnerOrTeacherForGet(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):

        if request.method == "GET":
            return request.user.role == "Owner" or request.user.role == "Teacher" or request.user.is_superuser
        return True


class IsAccountRoleOwnerForPost(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):

        if request.method == "POST":
            return request.user.role == "Owner" or request.user.is_superuser
        return True


class IsAccountHasSchool(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        return request.user.school_id is not None


class IsAuthenticatedAndAdmin(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: Account):
        return request.user.is_superuser and request.user.is_authenticated


class IsRoleOwnerOrObjOwnerOrAdm(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj) -> bool:
        school_id = request.user.school_id
        # school_id = view.kwargs.get('school_id')

        if request.user.is_superuser or request.user.role == 'Owner':
            return True

        if isinstance(obj, School):
            return request.user == obj.account

        if isinstance(obj, (Account, Course)):
            return request.user == obj.school.account and obj.school.id == school_id

        if isinstance(obj, Class):
            return request.user == obj.course.school.account and obj.course.school.id == school_id

        if isinstance(obj, (ClassRegistration, Attendance, TestResult)):
            return request.user == obj.account and obj.account.school_id == school_id

        if isinstance(obj, Classroom):
            return request.user == obj.cclass.course.school.account and obj.cclass.course.school.id == school_id

        if isinstance(obj, (Test, Occurrence)):
            return request.user == obj.classroom.cclass.course.school.account and obj.classroom.cclass.course.school.id == school_id