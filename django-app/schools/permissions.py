from rest_framework.views import Request, View
from schools.models import School
from teachers.models import Teacher
from students.models import Student, ClassRegistration, Attendance, TestResult
from courses.models import Course
from classes.models import Class
from classrooms.models import Classroom
from ttests.models import Test

from rest_framework import permissions


class IsAdminOrSchoolOwner(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj) -> bool:
        school_id = view.kwargs.get('school_id')

        if request.user.is_superuser:
            return True

        if isinstance(obj, School):
            return request.user == obj.account

        if isinstance(obj, (Teacher, Student, Course)):
            return request.user == obj.school.account and obj.school.id == school_id

        if isinstance(obj, Class):
            return request.user == obj.course.school.account and obj.course.school.id == school_id

        if isinstance(obj, (ClassRegistration, Attendance, TestResult)):
            return request.user == obj.student.school.account and obj.student.school.id == school_id

        if isinstance(obj, Classroom):
            return request.user == obj.cclass.course.school.account and obj.cclass.course.school.id == school_id

        if isinstance(obj, Test):
            return request.user == obj.classroom.cclass.course.school.account and obj.classroom.cclass.course.school.id == school_id
