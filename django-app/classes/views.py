from rest_framework import generics
from .models import Class
from .serializers import ClassSerializer, ClassCreateSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from accounts.permissions import IsAccountRoleOwnerOrAdmin, IsAccountRoleOwner
from schools.permissions import IsAdminOrSchoolOwner
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from courses.models import Course
from schools.models import School
from schools.mixins import SchoolPermissionMixin
from rest_framework.exceptions import NotFound, ValidationError


class ClassView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAccountRoleOwner()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ClassCreateSerializer
        return ClassSerializer

    def get_queryset(self):
        school_id = self.request.user.school_id

        if self.request.user.is_superuser:
            return Class.objects.all()

        elif self.request.user.role == 'Student':
            student_id = self.request.user.student_id
            return Class.objects.filter(
                class_registration__student__student_id=student_id,
                course__school_id=school_id,
            )
        return Class.objects.filter(course__school_id=school_id)

    def perform_create(self, serializer):

        school_id = self.request.user.school_id
        course_id = self.request.data.get('course_id')

        find_course = Course.objects.filter(
            school_id=school_id,
            pk=course_id,
        ).first()
        if not find_course:
            raise NotFound("Course not found")

        serializer.save(course_id=course_id,)


class ClassDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAccountRoleOwnerOrAdmin()]

    serializer_class = ClassSerializer

    lookup_url_kwarg = "class_id"

    def get_queryset(self):
        school_id = self.request.user.school_id
        class_id = self.kwargs[self.lookup_url_kwarg]

        if self.request.user.is_superuser:
            return Class.objects.filter(pk=class_id)

        elif self.request.user.role == 'Student':
            student_id = self.request.user.student_id
            return Class.objects.filter(
                class_registration__student__student_id=student_id,
                course__school_id=school_id,
                pk=class_id
            )
        return Class.objects.filter(
            course__school_id=school_id,
            pk=self.kwargs[self.lookup_url_kwarg]
        )

    def perform_update(self, serializer):
        school_id = self.request.user.school_id
        course_id = self.request.data.get('course_id')

        if course_id:
            find_course = Course.objects.filter(
                pk=course_id,
                school_id=school_id
            )
            if not find_course:
                NotFound("Course not found")
            serializer.save(course_id=course_id)

        serializer.save()

    def perform_destroy(self, instance: Class):
        instance.is_active = False
        instance.save()
