from rest_framework import generics
from .models import Class
from .serializers import ClassSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from schools.permissions import IsAdminOrSchoolOwner
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from schools.models import School
from schools.mixins import SchoolPermissionMixin


# Voltar aqui quando conf app classes
class ClassView(SchoolPermissionMixin, generics.ListCreateAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated, IsAdminOrSchoolOwner]

    queryset = Class.objects.all()
    serializer_class = ClassSerializer

    school_url_kwarg = 'school_id'

    def get_queryset(self):
        school_id = self.kwargs[self.school_url_kwarg]
        return Class.objects.filter(course__school_id=school_id)

    def perform_create(self, serializer):
        # Acertar
        school_id = self.kwargs[self.school_url_kwarg]
        Class.objects.filter(
            course__school_id=school_id,
            course_id=
        )
        serializer.save(school_id=school_id)

    # def get_object(self)


class ClassDetailView(generics.RetrieveUpdateDestroyAPIView):
    ...
