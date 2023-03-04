from .models import School
from .serializers import SchoolSerializer
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from accounts.permissions import IsAccountOwnerOrAdmin
from .permissions import IsAdminOrSchoolOwner
from rest_framework.permissions import IsAuthenticated


# Ambas rotas funcionando com as permissões esperadas
# No momento de criação, apenas se criam escolas para a conta que está autenticada.
class SchoolView(generics.ListCreateAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOwnerOrAdmin]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return School.objects.all()
        return School.objects.filter(account=self.request.user)

    # queryset = School.objects.all()
    serializer_class = SchoolSerializer

    def perform_create(self, serializer):
        serializer.save(account=self.request.user)


class SchoolDetailView(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrSchoolOwner]

    queryset = School.objects.all()
    serializer_class = SchoolSerializer

    lookup_url_kwarg = "school_id"
