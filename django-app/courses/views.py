from rest_framework import generics
from .models import Course
from .serializers import CourseSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from schools.permissions import IsAdminOrSchoolOwner
from accounts.permissions import IsAccountRoleOwnerOrAdmin
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from schools.models import School
from schools.mixins import SchoolPermissionMixin


class CourseView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated, IsAdminOrSchoolOwner]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAccountRoleOwnerOrAdmin()]

    # queryset = Course.objects.all()
    serializer_class = CourseSerializer

    # school_url_kwarg = 'school_id'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Course.objects.all()
        # school_id = self.kwargs['school_id']
        school_id = self.request.user.school_id
        return Course.objects.filter(school_id=school_id)

    def perform_create(self, serializer):
        school_id = self.request.user.school_id
        serializer.save(school_id=school_id)


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated, IsAdminOrSchoolOwner,]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAccountRoleOwnerOrAdmin()]

    serializer_class = CourseSerializer

    lookup_url_kwarg = "course_id"

    def get_queryset(self):
        school_id = self.request.user.school_id

        if self.request.user.is_superuser:
            return Course.objects.filter(pk=self.kwargs[self.lookup_url_kwarg])
        return Course.objects.filter(school_id=school_id, pk=self.kwargs[self.lookup_url_kwarg])

    def perform_destroy(self, instance: Course):
        instance.is_active = False
        instance.save()
