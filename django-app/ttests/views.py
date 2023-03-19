from rest_framework import generics
from .models import Test
from .serializers import TestSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from accounts.permissions import IsAccountRoleOwnerOrAdmin
from schools.permissions import IsAdminOrSchoolOwner
from rest_framework.permissions import IsAuthenticated
from classrooms.models import Classroom
from classes.models import Class
from courses.models import Course
from schools.models import School
from schools.mixins import SchoolPermissionMixin
from rest_framework.exceptions import NotFound


class TestView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAccountRoleOwnerOrAdmin()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TestCreateSerializer
        return TestSerializer

    def get_queryset(self):
        school_id = self.request.user.school_id

        if self.request.user.is_superuser:
            return Test.objects.all()

        elif self.request.user.role == 'Student':
            student_id = self.request.user.student_id
            return Test.objects.filter(
                classroom__cclass__course__school_id=school_id,
                classroom__cclass__class_registration__student__student_id=student_id
            )

        elif self.request.user.role == 'Teacher':
            teacher_id = self.request.user.teacher_id
            return Test.objects.filter(
                classroom__cclass__course__school_id=school_id,
                classroom__teacher_id=teacher_id
            )

        return Test.objects.filter(
            classroom__cclass__course__school_id=school_id,
        )

    def perform_create(self, serializer):

        school_id = self.request.user.school_id
        classroom_id = self.request.data.get('classroom_id')

        find_classroom = Classroom.objects.filter(
            pk=classroom_id,
            cclass__course__school_id=school_id
        ).first()
        if not find_classroom:
            raise NotFound("Classroom not found")

        serializer.save(classroom_id=classroom_id,)


class TestDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAccountRoleOwnerOrAdmin()]

    serializer_class = TestSerializer

    lookup_url_kwarg = "test_id"

    def get_queryset(self):
        school_id = self.request.user.school_id
        test_id = self.kwargs[self.lookup_url_kwarg]

        if self.request.user.is_superuser:
            return Test.objects.filter(pk=test_id)

        elif self.request.user.role == 'Teacher':
            teacher_id = self.request.user.teacher_id
            return Test.objects.filter(
                classroom__cclass__course__school_id=school_id,
                pk=test_id,
                classroom__teacher_id=teacher_id
            )

        elif self.request.user.role == 'Student':
            student_id = self.request.user.student_id
            return Test.objects.filter(
                classroom__cclass__course__school_id=school_id,
                pk=test_id,
                classroom__cclass__class_registration__student__student_id=student_id
            )

        return Test.objects.filter(
            classroom__cclass__course__school_id=school_id, 
            pk=self.kwargs[self.lookup_url_kwarg]
        )

    def perform_update(self, serializer):
        school_id = self.request.user.school_id
        classroom_id = self.request.data.get('classroom_id')

        if classroom_id:
            find_classroom = Classroom.objects.filter(
                pk=classroom_id,
                cclass__course__school_id=school_id
            ).first()
            if not find_classroom:
                raise NotFound("Classroom not found.")
            serializer.save(classroom_id=classroom_id)

        serializer.save()

    # Teste Git

    # def perform_destroy(self, instance: Test):
    #     instance.is_active = False
    #     instance.save()
