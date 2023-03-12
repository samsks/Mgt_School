from .models import Account
from accounts import serializers
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsAccountOwnerOrAdmin, IsAuthenticatedAndAdmin, IsAccountRoleOwnerOrAdmin, IsAccountHasSchool
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from schools.mixins import SchoolPermissionMixin
from rest_framework.exceptions import ValidationError
import ipdb


# Estado atual: Listando todas as contas abertamente
# Filtrando apenas users ativos
# last login not implemented

# opções necessárias para essa view:
# Listar todas as contas como admin - permissoes de autenticado e admin

# Listar todas as contas como professor - permissoes de autenticado, ligação com a escola específica.
# ...Filtro apenas da escola e 'Student.class_registration.class.classroom == teacher.classroom,
# ...ocultando role Owner, mostrando 'Students'

# OWNER VIEWS ------------------------------------------------------------------------------------------
class AccountOwnerListView(SchoolPermissionMixin, generics.ListAPIView):
    # Função: Listar todas as contas como owner
    # Permissões: autenticado e dono da escola específica.
    # Filtro: apenas da escola que criou
    # Extras: Acrescentar query and params for only students or teachers
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOwnerOrAdmin]

    school_url_kwarg = 'school_id'

    # queryset = Account.objects.all()
    # Serializer individual mostrando todos os campos para students e teachers
    serializer_class = serializers.AccountOwnerSerializer

    def get_queryset(self):
        school_id = self.kwargs[self.school_url_kwarg]
        return Account.objects.filter(school_id=school_id)


class AccountOwnerCreateView(generics.CreateAPIView):
    # Função: Criar um usuário Owner, padrão no sistema
    # Permissões: Nenhuma
    # Filtro: Nenhum
    # Extras: Nenhum

    queryset = Account.objects.all()
    # Serializer individual personalizado para role Owner
    serializer_class = serializers.AccountOwnerCreateSerializer


# Verificar
class AccountDetailView(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOwnerOrAdmin,]

    queryset = Account.objects.all()
    serializer_class = serializers.AccountOwnerSerializer

    lookup_url_kwarg = "account_id"


# TEACHER VIEWS --------------------------------------------------------------------------
class AccountTeacherView(generics.ListCreateAPIView):
    # Função: Listar todas as contas da role professor
    # Permissões: autenticado, dono da escola específica e ter a role Owner.
    # Filtro: apenas da escola que criou
    # Extras: Acrescentar query and params para campos como is_active, fired_at, major, etc
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountRoleOwnerOrAdmin]

    # queryset = Account.objects.filter(role='Teacher')
    serializer_class = serializers.AccountTeacherSerializer

    def get_queryset(self):
        school_id = self.request.user.school_id

        if self.request.user.is_superuser:
            return Account.objects.all()
        elif self.request.user.school_id is None:
            raise ValidationError({'message': 'It is necessary to register a school before having teachers and students.'})
        return Account.objects.filter(school_id=school_id, role='Teacher')


# class AccountTeacherCreateView(generics.CreateAPIView):
#     # Função: Criar uma conta da role professor
#     # Permissões: autenticado, dono da escola específica , ter a role Owner.
#     # Filtro: apenas da escola que criou
#     # Extras: Nenhum
#     queryset = Account.objects.filter(is_active=True, role='Teacher')
#     # Serializer compartilhado entre List e Create mostrando todos os campos para teachers
#     serializer_class = serializers.AccountTeacherSerializer


# STUDENT VIEWS ------------------------------------------------------------------------------------
class AccountStudentView(generics.ListCreateAPIView):
    # Função: Listar todas as contas da role student
    # Permissões: autenticado, dono da escola específica e ter a role Owner.
    # Filtro: apenas da escola que criou
    # Extras: Acrescentar query and params para campos como is_active, class_id, etc

    queryset = Account.objects.filter(role='Student')
    # Serializer compartilhado entre List e Create mostrando todos os campos para students
    serializer_class = serializers.AccountStudentSerializer


class AccountTeacherCreateView(generics.CreateAPIView):
    # Função: Criar uma conta da role student
    # Permissões: autenticado, dono da escola específica, ter a role Owner.
    # Filtro: apenas da escola que criou
    # Extras: Nenhum
    queryset = Account.objects.filter(is_active=True)
    # Serializer compartilhado entre List e Create mostrando todos os campos para students
    serializer_class = serializers.AccountStudentSerializer
