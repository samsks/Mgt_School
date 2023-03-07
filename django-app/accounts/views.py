from .models import Account
from .serializers import AccountSerializer
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsAccountOwnerOrAdmin, IsAuthenticatedAndAdmin
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
import ipdb


# Estado atual: Listando todas as contas abertamente
# Filtrando apenas users ativos
# last login not implemented
class AccountView(generics.ListCreateAPIView):

    queryset = Account.objects.filter(is_active=True)
    serializer_class = AccountSerializer


class AccountDetailView(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOwnerOrAdmin,]

    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    lookup_url_kwarg = "account_id"
