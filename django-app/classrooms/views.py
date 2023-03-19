from rest_framework import generics
from .models import Classroom
from .serializers import ClassroomSerializer, ClassroomCreateSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from accounts.permissions import IsAccountRoleOwnerOrAdmin, IsAccountRoleOwner
from schools.permissions import IsAdminOrSchoolOwner
from rest_framework.permissions import IsAuthenticated
from accounts.models import Account
from classes.models import Class
from courses.models import Course
from schools.models import School
from schools.mixins import SchoolPermissionMixin
from rest_framework.exceptions import NotFound
from utils.function_account import validate_uuid


class ClassroomView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAccountRoleOwner()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ClassroomCreateSerializer
        return ClassroomSerializer

    def get_queryset(self):
        school_id = self.request.user.school_id

        if self.request.user.is_superuser:
            return Classroom.objects.all()

        elif self.request.user.role == 'Student':
            student_id = self.request.user.student_id
            return Classroom.objects.filter(
                cclass__class_registration__student__student_id=student_id,
                cclass__course__school_id=school_id
            )

        elif self.request.user.role == 'Teacher':
            teacher_id = self.request.user.teacher_id
            return Classroom.objects.filter(
                teacher_id=teacher_id,
                cclass__course__school_id=school_id
            )

        return Classroom.objects.filter(
            cclass__course__school_id=school_id,
        )

    def perform_create(self, serializer):

        school_id = self.request.user.school_id
        class_id = self.request.data.get('class_id')
        teacher_id = self.request.data.get('teacher_id')

        find_class = Class.objects.filter(
            pk=class_id,
            course__school_id=school_id
        ).first()
        if not find_class:
            raise NotFound("Class not found")

        if teacher_id:
            validate_uuid(teacher_id)
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

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return ClassroomCreateSerializer
        return ClassroomSerializer

    lookup_url_kwarg = "classroom_id"

    def get_queryset(self):
        school_id = self.request.user.school_id
        classroom_id = self.kwargs[self.lookup_url_kwarg]

        if self.request.user.is_superuser:
            return Classroom.objects.filter(pk=classroom_id)

        elif self.request.user.role == 'Teacher':
            teacher_id = self.request.user.teacher_id
            return Classroom.objects.filter(
                teacher_id=teacher_id,
                cclass__course__school_id=school_id,
                pk=classroom_id
            )
        elif self.request.user.role == 'Student':
            student_id = self.request.user.student_id
            return Classroom.objects.filter(
                cclass__class_registration__student__student_id=student_id,
                cclass__course__school_id=school_id,
                pk=classroom_id
            )
        return Classroom.objects.filter(
            cclass__course__school_id=school_id,
            pk=self.kwargs[self.lookup_url_kwarg]
        )

    def perform_update(self, serializer):
        school_id = self.request.user.school_id
        class_id = self.request.data.get('class_id')
        teacher_id = self.request.data.get('teacher_id')
        kwargs = {}

        if class_id:
            find_class = Class.objects.filter(
                pk=class_id,
                course__school_id=school_id
            ).first()
            if not find_class:
                raise NotFound("Class not found")
            kwargs['class_id'] = class_id

        if teacher_id:
            validate_uuid(teacher_id)
            find_teacher = Account.objects.filter(
                teacher_id=teacher_id,
                role='Teacher',
                school_id=school_id
            ).first()
            if not find_teacher:
                raise NotFound("Teacher not found")
            kwargs['teacher_id'] = teacher_id

        if kwargs:
            serializer.save(**kwargs)
        serializer.save()

    def perform_destroy(self, instance: Classroom):
        instance.is_active = False
        instance.save()
