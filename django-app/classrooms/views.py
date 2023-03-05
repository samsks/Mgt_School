from rest_framework import generics
from .models import Classroom
from .serializers import ClassroomSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from schools.permissions import IsAdminOrSchoolOwner
from rest_framework.permissions import IsAuthenticated
from classes.models import Class
from courses.models import Course
from schools.models import School
from schools.mixins import SchoolPermissionMixin
from rest_framework.exceptions import NotFound


# Voltar aqui quando conf app classes
class ClassroomView(SchoolPermissionMixin, generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrSchoolOwner]

    # queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer

    school_url_kwarg = 'school_id'

    def get_queryset(self):
        school_id = self.kwargs[self.school_url_kwarg]
        course_id = self.request.data.get('course_id')
        return Classroom.objects.filter(
            _class__course__school_id=school_id,
            # _class__course_id=course_id,
        )

    def perform_create(self, serializer):

        school_id = self.kwargs[self.school_url_kwarg]
        course_id = self.request.data.get('course_id')
        class_id = self.request.data.get('class_id')

        find_school = School.objects.filter(pk=school_id).first()
        if not find_school:
            raise NotFound("School not found")

        find_course = Course.objects.filter(
            school_id=school_id,
            pk=course_id,
        ).first()
        if not find_course:
            raise NotFound("Course not found")

        find_class = Class.objects.filter(
            pk=class_id,
            course=course_id,
            course__school_id=school_id
        ).first()
        if not find_class:
            raise NotFound("Class not found")

        serializer.save(_class_id=class_id,)


class ClassroomDetailView(generics.RetrieveUpdateDestroyAPIView):
    ...
