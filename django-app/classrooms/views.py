from rest_framework import generics
from .models import Classroom
from .serializers import ClassroomSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from accounts.permissions import IsAccountRoleOwnerOrAdmin
from schools.permissions import IsAdminOrSchoolOwner
from rest_framework.permissions import IsAuthenticated
from classes.models import Class
from courses.models import Course
from schools.models import School
from schools.mixins import SchoolPermissionMixin
from rest_framework.exceptions import NotFound


class ClassroomView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAccountRoleOwnerOrAdmin()]

    serializer_class = ClassroomSerializer

    # school_url_kwarg = 'school_id'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Classroom.objects.all()
        school_id = self.request.user.school_id
        return Classroom.objects.filter(
            cclass__course__school_id=school_id,
        )

    def perform_create(self, serializer):

        school_id = self.request.user.school_id
        class_id = self.request.data.get('class_id')
        teacher_id = self.request.data.get('teacher_id')

        # find_school = School.objects.filter(pk=school_id).first()
        # if not find_school:
        #     raise NotFound("School not found")

        find_class = Class.objects.filter(
            pk=class_id,
            course__school_id=school_id
        ).first()
        if not find_class:
            raise NotFound("Class not found")

        if teacher_id:
            find_teacher = Account.objects.filter(
                teacher_id=teacher_id,
                role='Teacher',
                school_id=school_id
            ).first()
            if not find_teacher:
                raise NotFound("Teacher not found")
            serializer.save(cclass_id=class_id, teacher_id=teacher_id,)

        serializer.save(cclass_id=class_id,)


class ClassroomDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAccountRoleOwnerOrAdmin()]

    serializer_class = ClassroomSerializer

    lookup_url_kwarg = "classroom_id"

    def get_queryset(self):
        school_id = self.request.user.school_id

        if self.request.user.is_superuser:
            return Classroom.objects.filter(pk=self.kwargs[self.lookup_url_kwarg])
        return Classroom.objects.filter(cclass__course__school_id=school_id, pk=self.kwargs[self.lookup_url_kwarg])

    def perform_destroy(self, instance: Classroom):
        instance.is_active = False
        instance.save()
