from rest_framework import generics
from .models import Teacher
from .serializers import TeacherSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from schools.permissions import IsAdminOrSchoolOwner
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from schools.models import School
from schools.mixins import SchoolPermissionMixin


class TeacherView(SchoolPermissionMixin, generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrSchoolOwner]

    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    school_url_kwarg = 'school_id'

    def get_queryset(self):
        school_id = self.kwargs['school_id']
        return Teacher.objects.filter(school_id=school_id)

    def perform_create(self, serializer):
        school_id = self.kwargs['school_id']
        serializer.save(school_id=school_id)


class TeacherDetailView(generics.RetrieveUpdateDestroyAPIView):
    ...
