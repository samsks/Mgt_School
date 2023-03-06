from rest_framework import generics
from .models import Class
from .serializers import ClassSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from schools.permissions import IsAdminOrSchoolOwner
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from courses.models import Course
from teachers.models import Teacher
from schools.models import School
from schools.mixins import SchoolPermissionMixin
from rest_framework.exceptions import NotFound


class ClassView(SchoolPermissionMixin, generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrSchoolOwner]

    serializer_class = ClassSerializer

    school_url_kwarg = 'school_id'

    def get_queryset(self):
        school_id = self.kwargs[self.school_url_kwarg]
        return Class.objects.filter(course__school_id=school_id)

    def perform_create(self, serializer):

        school_id = self.kwargs[self.school_url_kwarg]
        course_id = self.request.data.get('course_id')
        teacher_id = self.request.data.get('teacher_id')

        find_school = School.objects.filter(pk=school_id).first()
        if not find_school:
            raise NotFound("School not found")

        find_course = Course.objects.filter(
            school_id=school_id,
            pk=course_id,
        ).first()
        if not find_course:
            raise NotFound("Course not found")

        if teacher_id:
            find_teacher = Teacher.objects.filter(
                pk=teacher_id,
                school_id=school_id
            ).first()
            if not find_teacher:
                raise NotFound("Teacher not found")
            serializer.save(course_id=course_id, teacher_id=teacher_id,)

        serializer.save(course_id=course_id,)


class ClassDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrSchoolOwner,]

    queryset = Class.objects.all()
    serializer_class = ClassSerializer

    lookup_url_kwarg = "class_id"
