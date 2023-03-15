from rest_framework import generics
from .models import Occurrence
from .serializers import OccurrenceSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from accounts.permissions import IsAccountRoleOwnerOrAdmin
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound


class OccurrenceView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated, IsAdminOrSchoolOwner]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAccountRoleOwnerOrAdmin()]

    serializer_class = OccurrenceSerializer

    # school_url_kwarg = 'school_id'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Occurrence.objects.all()
        school_id = self.request.user.school_id
        return Occurrence.objects.filter(
            classroom__cclass__course__school_id=school_id,
        )

    def perform_create(self, serializer):

        school_id = self.request.user.school_id
        classroom_id = self.request.data.get('classroom_id')

        # find_school = School.objects.filter(pk=school_id).first()
        # if not find_school:
        #     raise NotFound("School not found")

        find_classroom = Classroom.objects.filter(
            pk=classroom_id,
            cclass__course__school_id=school_id
        ).first()
        if not find_classroom:
            raise NotFound("Classroom not found")

        serializer.save(classroom_id=classroom_id,)


class OccurrenceDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAccountRoleOwnerOrAdmin()]

    serializer_class = OccurrenceSerializer

    lookup_url_kwarg = "occurrence_id"

    def get_queryset(self):
        school_id = self.request.user.school_id

        if self.request.user.is_superuser:
            return Test.objects.filter(pk=self.kwargs[self.lookup_url_kwarg])
        return Test.objects.filter(classroom__cclass__course__school_id=school_id, pk=self.kwargs[self.lookup_url_kwarg])

    # def perform_destroy(self, instance: Account):
    #     instance.is_active = False
    #     instance.save()
