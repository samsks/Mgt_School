from rest_framework import generics
from rest_framework.views import Response, status
from .models import Student, ClassRegistration, TestResult, Attendance
from .serializers import StudentSerializer, ClassRegistrationSerializer, TestResultSerializer, AttendanceSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from schools.permissions import IsAdminOrSchoolOwner
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from schools.models import School
from schools.mixins import SchoolPermissionMixin
from classes.models import Class
from classrooms.models import Classroom
from ttests.models import Test
from rest_framework.exceptions import NotFound, ValidationError


# Voltar aqui quando conf app classes
class StudentView(SchoolPermissionMixin, generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrSchoolOwner]

    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    school_url_kwarg = 'school_id'

    def get_queryset(self):
        school_id = self.kwargs['school_id']
        return Student.objects.filter(school_id=school_id)

    def perform_create(self, serializer):
        school_id = self.kwargs['school_id']
        serializer.save(school_id=school_id)


class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    ...


class ClassRegistrationView(SchoolPermissionMixin, generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrSchoolOwner]

    queryset = ClassRegistration.objects.all()
    serializer_class = ClassRegistrationSerializer

    school_url_kwarg = 'school_id'

    def get_queryset(self):
        school_id = self.kwargs['school_id']
        return ClassRegistration.objects.filter(student__school_id=school_id)

    def perform_create(self, serializer):
        school_id = self.kwargs[self.school_url_kwarg]
        class_id = self.request.data.get('class_id')
        student_id = self.request.data.get('student_id')

        find_school = School.objects.filter(pk=school_id).first()
        if not find_school:
            raise NotFound("School not found")

        find_student = Student.objects.filter(
            school_id=school_id,
            pk=student_id,
        ).first()
        if not find_student:
            raise NotFound("Student not found")

        find_class = Class.objects.filter(
            pk=class_id,
            course__school_id=school_id
        ).first()
        if not find_class:
            raise NotFound("Class not found")

        serializer.save(student_id=student_id, cclass_id=class_id)


class ClassRegistrationDetailView(SchoolPermissionMixin, generics.ListCreateAPIView):
    ...


class TestResultView(SchoolPermissionMixin, generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrSchoolOwner]

    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer

    school_url_kwarg = 'school_id'

    def get_queryset(self):
        school_id = self.kwargs['school_id']
        return TestResult.objects.filter(student__school_id=school_id)

    def perform_create(self, serializer):
        school_id = self.kwargs[self.school_url_kwarg]
        test_id = self.request.data.get('test_id')
        student_id = self.request.data.get('student_id')

        find_school = School.objects.filter(pk=school_id).first()
        if not find_school:
            raise NotFound("School not found")

        find_student = Student.objects.filter(
            school_id=school_id,
            pk=student_id,
        ).first()
        if not find_student:
            raise NotFound("Student not found")

        find_test = Test.objects.filter(
            pk=test_id,
            classroom__cclass__course__school_id=school_id
        ).first()
        if not find_test:
            raise NotFound("Test not found")

        serializer.save(student_id=student_id, test_id=test_id)


class TestResultDetailView(SchoolPermissionMixin, generics.ListCreateAPIView):
    ...


class AttendanceView(SchoolPermissionMixin, generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrSchoolOwner]

    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    school_url_kwarg = 'school_id'

    def get_queryset(self):
        school_id = self.kwargs['school_id']
        return Attendance.objects.filter(student__school_id=school_id)

    def perform_create(self, serializer):
        school_id = self.kwargs[self.school_url_kwarg]
        classroom_id = self.request.data.get('classroom_id')
        student_id = self.request.data.get('student_id')

        find_school = School.objects.filter(pk=school_id).first()
        if not find_school:
            raise NotFound("School not found")

        find_student = Student.objects.filter(
            school_id=school_id,
            pk=student_id,
        ).first()
        if not find_student:
            raise NotFound("Student not found")

        find_classroom = Classroom.objects.filter(
            pk=classroom_id,
            cclass__course__school_id=school_id
        ).first()
        if not find_classroom:
            raise NotFound("Classroom not found")

        # Check de presença para um update. Removendo pois não faz sentido sem determinar as aulas e identificar individualmente
        # find_attendance = Attendance.objects.filter(
        #     classroom_id=classroom_id,
        #     student_id=student_id,
        #     classroom__cclass__course__school_id=school_id
        # ).first()
        # if find_attendance:
        #     raise ValidationError("Registro de presença encontrado")

        serializer.save(student_id=student_id, classroom_id=classroom_id)


class AttendanceDetailView(SchoolPermissionMixin, generics.ListCreateAPIView):
    ...
