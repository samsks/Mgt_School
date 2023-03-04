from .models import Account
from .serializers import AccountSerializer
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsAccountOwnerOrAdmin, IsAuthenticatedAndAdmin
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
import ipdb


# Estado atual: Listando todas as contas abertamente
# Filtrando apenas users ativos
class AccountView(generics.ListCreateAPIView):

    # def get_authenticators(self):
    #     if self.request.method == 'GET':
    #         return [JWTAuthentication]
    #     return super().get_authenticators()

    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [IsAuthenticatedAndAdmin]
    #     elif self.request.method == 'POST':
    #         return [AllowAny()]
    #     return super().get_permissions()

    # authentication_classes = get_authenticators
    # permission_classes = get_permissions

    queryset = Account.objects.filter(is_active=True)
    serializer_class = AccountSerializer


# Estado atual: Funcionando por dono ou admin 
# Excluindo normalmente, descomentar antes de subir
class AccountDetailView(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOwnerOrAdmin,]

    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    lookup_url_kwarg = "account_id"

    # def perform_destroy(self, instance: Account):
    #     instance.is_active = False
    #     instance.save()
