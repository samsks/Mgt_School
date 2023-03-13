from .models import Account
from schools.models import School
from accounts import serializers
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsAccountOwnerOrAdmin, IsAuthenticatedAndAdmin, IsAccountRoleOwnerOrAdmin, IsAccountHasSchool, IsAccountRoleOwnerOrTeacherForGet, IsAccountRoleOwnerForPost, IsAccountRoleTeacherOrAdmin
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

class AccountOwnerListView(generics.ListAPIView):
    # VERIFICAR SE POSSIVEL JUNTAR COM CREATE E USAR SERIALIZERS DIFERENTES

    # Função: Listar todas as contas de uma escola como owner
    # Permissões: autenticado e dono da escola específica.
    # Filtro: apenas da escola que criou
    # Extras: Acrescentar query and params for only students or teachers
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountRoleOwnerOrAdmin]

    school_url_kwarg = 'school_id'

    # queryset = Account.objects.all()
    # Serializer individual mostrando todos os campos para students e teachers
    serializer_class = serializers.AccountOwnerSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            school_id = self.kwargs[self.school_url_kwarg]
        else:
            school_id = self.request.user.school_id
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
    permission_classes = [IsAuthenticated, IsAccountRoleOwnerOrAdmin,]

    serializer_class = serializers.AccountOwnerDetailSerializer

    lookup_url_kwarg = "account_id"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Account.objects.filter(pk=self.kwargs[self.lookup_url_kwarg])
        else:
            school_id = self.request.user.school_id
        return Account.objects.filter(school_id=school_id)

    def perform_destroy(self, instance: Account):
        if instance.role == 'Owner':

            school_obj = School.objects.filter(pk=instance.school_id).first()
            if school_obj:
                school_obj.is_active = False
                school_obj.save()

            # DESATIVA TODOS OS USUÁRIOS LIGADOS A ESCOLA. ELABORAR UMA SOLUÇÃO MELHOR
            # list__accounts = Account.objects.filter(school_id=instance.school_id, is_active=True)
            # for account in list_accounts:
            #     account.is_active = False
            #     account.save()

        instance.is_active = False
        instance.save()


# TEACHER VIEWS --------------------------------------------------------------------------
class AccountTeacherView(generics.ListCreateAPIView):
    # Função: Listar todas as contas da role professor
    # Permissões: autenticado, dono da escola específica e ter a role Owner.
    # Filtro: apenas da escola que criou
    # Extras: Acrescentar query and params para campos como is_active, fired_at, major, etc
    authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated, IsAccountRoleOwnerOrAdmin]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAccountRoleOwnerOrAdmin()]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.AccountTeacherListSerializer
        return serializers.AccountTeacherCreateSerializer

    def get_queryset(self):
        school_id = self.request.user.school_id

        if self.request.user.is_superuser:
            return Account.objects.all()
        elif self.request.user.school_id is None:
            raise ValidationError({'message': 'It is necessary to register a school before having teachers and students.'})
        return Account.objects.filter(school_id=school_id, role='Teacher', is_active=True)


class AccountTeacherDetailView(generics.RetrieveUpdateDestroyAPIView):
    # Função: Listar todas as contas da role professor
    # Permissões: autenticado, dono da escola específica e ter a role Owner.
    # Filtro: apenas da escola que criou
    # Extras: Acrescentar query and params para campos como is_active, fired_at, major, etc
    authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated, IsAccountRoleOwnerOrAdmin]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method == 'PATCH':
            return [IsAuthenticated(), IsAccountOwnerOrAdmin()]
        return [IsAuthenticated(), IsAccountRoleOwnerOrAdmin()]

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return serializers.AccountTeacherUpdateSerializer
        return serializers.AccountTeacherListSerializer

    lookup_url_kwarg = "account_id"

    def get_queryset(self):
        school_id = self.request.user.school_id

        if self.request.user.is_superuser:
            return Account.objects.filter(pk=self.kwargs[self.lookup_url_kwarg])
        elif self.request.user.school_id is None:
            raise ValidationError({'message': 'It is necessary to register a school before having teachers and students.'})
        # elif self.request.user.role is "Owner":
        #     return Account.objects.filter(school_id=school_id, role='Teacher')
        return Account.objects.filter(school_id=school_id, role='Teacher', is_active=True)

    def perform_destroy(self, instance: Account):
        instance.is_active = False
        instance.save()


# STUDENT VIEWS ------------------------------------------------------------------------------------
class AccountStudentView(generics.ListCreateAPIView):
    # Função: Listar todas as contas da role student
    # Permissões: autenticado, dono da escola específica e ter a role Owner.
    # Filtro: apenas da escola que criou
    # Extras: Acrescentar query and params para campos como is_active, student_code, etc
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountRoleOwnerOrTeacherForGet, IsAccountRoleOwnerForPost]

    # queryset = Account.objects.filter(role='Teacher')

    # Serializer compartilhado entre List e Create mostrando todos os campos para students
    serializer_class = serializers.AccountStudentSerializer

    def get_queryset(self):
        school_id = self.request.user.school_id

        if self.request.user.is_superuser:
            return Account.objects.all()
        elif self.request.user.school_id is None:
            raise ValidationError({'message': 'It is necessary to register a school before having teachers and students.'})
        # colocar relacionamento com suas aulas
        elif self.request.user.role == 'Teacher':
            return Account.objects.filter(school_id=school_id, role='Student', )
        return Account.objects.filter(school_id=school_id, role='Student')


# class AccountTeacherCreateView(generics.CreateAPIView):
#     # Função: Criar uma conta da role student
#     # Permissões: autenticado, dono da escola específica, ter a role Owner.
#     # Filtro: apenas da escola que criou
#     # Extras: Nenhum
#     queryset = Account.objects.filter(is_active=True)
#     # Serializer compartilhado entre List e Create mostrando todos os campos para students
#     serializer_class = serializers.AccountStudentSerializer
