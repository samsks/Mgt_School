from .models import School
from .serializers import SchoolSerializer, SchoolOnlyInfoSerializer
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from accounts.permissions import IsAccountOwnerOrAdmin, IsAccountRoleOwnerOrAdmin
from .permissions import IsAdminOrSchoolOwner
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError


class SchoolView(generics.ListCreateAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountRoleOwnerOrAdmin]

    serializer_class = SchoolSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return School.objects.all()
        return School.objects.filter(pk=self.request.user.school_id)

    def perform_create(self, serializer):
        account = self.request.user
        if account.school:
            raise ValidationError({'message': "Your account already has a school."})
        school = serializer.save()
        account.school = school
        account.save()


class SchoolDetailView(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated, IsAdminOrSchoolOwner]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAccountRoleOwnerOrAdmin()]

    def get_serializer_class(self):
        if self.request.method == 'GET' and self.request.user.role != 'Owner':
            return SchoolOnlyInfoSerializer
        return SchoolSerializer

    lookup_url_kwarg = "school_id"

    def get_queryset(self):
        school_id = self.kwargs[self.lookup_url_kwarg]

        if self.request.user.is_superuser:
            return School.objects.filter(pk=self.kwargs[self.lookup_url_kwarg])
        elif self.request.user.school_id is not school_id:
            raise ValidationError({'message': 'Invalid school identifier.'})
        return School.objects.filter(id=school_id)

    def perform_destroy(self, instance: School):
        instance.is_active = False
        instance.save()
