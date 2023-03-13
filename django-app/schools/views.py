from .models import School
from .serializers import SchoolSerializer
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
    permission_classes = [IsAuthenticated, IsAdminOrSchoolOwner]

    queryset = School.objects.all()
    serializer_class = SchoolSerializer

    lookup_url_kwarg = "school_id"
