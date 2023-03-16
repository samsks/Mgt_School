from .models import Account, ClassRegistration, TestResult, Attendance
from schools.models import School
from classes.models import Class
from accounts import serializers
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsAccountOwnerOrAdmin, IsAuthenticatedAndAdmin, IsAccountRoleOwnerOrAdmin, IsAccountHasSchool, IsAccountRoleOwnerOrTeacherForGet, IsAccountRoleOwnerForPost, IsAccountRoleTeacherOrAdmin
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from schools.mixins import SchoolPermissionMixin
from rest_framework.exceptions import ValidationError, NotFound
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
            if self.request.user.school_id is None:
                raise ValidationError({'message': 'It is necessary to register a school before listing accounts.'})

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
    permission_classes = [IsAuthenticated, IsAccountRoleOwnerOrAdmin]

    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [IsAuthenticated(), IsAccountRoleOwnerOrAdmin()]
    #     return [IsAuthenticated(), IsAccountRoleOwnerOrAdmin(), IsAccountOwnerOrAdmin()]

    serializer_class = serializers.AccountOwnerDetailSerializer

    lookup_url_kwarg = "account_id"

    def get_queryset(self):
        account_id = self.kwargs[self.lookup_url_kwarg]
        if self.request.user.is_superuser:
            return Account.objects.filter(pk=account_id)
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
            return Account.objects.filter(role='Teacher')
        elif self.request.user.school_id is None:
            raise ValidationError({'message': 'It is necessary to register a school before having teachers and students.'})
        return Account.objects.filter(school_id=school_id, role='Teacher', is_active=True)

    def perform_create(self, serializer):
        if self.request.user.school_id is None:
            raise ValidationError({'message': 'It is necessary to register a school before.'})
        serializer.save()


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
    # permission_classes = [IsAuthenticated, IsAccountRoleOwnerOrTeacherForGet, IsAccountRoleOwnerForPost]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAccountRoleOwnerOrAdmin()]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.AccountStudentListSerializer
        return serializers.AccountStudentCreateSerializer

    def get_queryset(self):
        school_id = self.request.user.school_id

        if self.request.user.is_superuser:
            return Account.objects.filter(role='Student')
        elif self.request.user.school_id is None:
            raise ValidationError({'message': 'It is necessary to register a school before having teachers and students.'})
        return Account.objects.filter(school_id=school_id, role='Student', is_active=True)

    def perform_create(self, serializer):
        if self.request.user.school_id is None:
            raise ValidationError({'message': 'It is necessary to register a school before.'})
        serializer.save()


class AccountStudentDetailView(generics.RetrieveUpdateDestroyAPIView):
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
            return serializers.AccountStudentUpdateSerializer
        return serializers.AccountStudentListSerializer

    lookup_url_kwarg = "account_id"

    def get_queryset(self):
        school_id = self.request.user.school_id

        if self.request.user.is_superuser:
            return Account.objects.filter(pk=self.kwargs[self.lookup_url_kwarg])
        elif self.request.user.school_id is None:
            raise ValidationError({'message': 'It is necessary to register a school before having teachers and students.'})
        # elif self.request.user.role is "Owner":
        #     return Account.objects.filter(school_id=school_id, role='Student')
        return Account.objects.filter(school_id=school_id, role='Student', is_active=True)

    def perform_destroy(self, instance: Account):
        instance.is_active = False
        instance.save()


# NOMEAR
class ClassRegistrationListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    # Ajeitar - Dono do objeto tbm pode
    permission_classes = [IsAuthenticated, IsAccountRoleOwnerOrAdmin]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated(), ]
        return [IsAuthenticated(), IsAccountRoleOwner()]

    serializer_class = serializers.ClassRegistrationSerializer

    student_url_kwarg = 'student_id'

    def get_queryset(self):
        student_id = self.kwargs['student_id']
        school_id = self.request.user.school_id
        if self.request.user.is_superuser:
            return ClassRegistration.objects.filter(student_id=student_id)
        return ClassRegistration.objects.filter(
            cclass__course__school_id=school_id,
            student_id=student_id
        )


class ClassRegistrationCreateView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    # Ajeitar
    permission_classes = [IsAuthenticated, IsAccountRoleOwnerOrAdmin]

    serializer_class = serializers.ClassRegistrationCreateSerializer

    def perform_create(self, serializer):
        school_id = self.request.user.school_id
        class_id = self.request.data.get('class_id')
        student_id = self.request.data.get('student_id')

        find_student = Account.objects.filter(
            school_id=school_id,
            student_id=student_id,
            role='Student',
        ).first()
        if not find_student:
            raise NotFound("Student not found")

        find_class = Class.objects.filter(
            pk=class_id,
            course__school_id=school_id
        ).first()
        if not find_class:
            raise NotFound("Class not found")

        serializer.save(student_id=student_id, cclass_id=class_id)


class ClassRegistrationDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountRoleOwnerOrAdmin,]

    serializer_class = serializers.ClassRegistrationSerializer

    lookup_url_kwarg = "class_register_id"

    def get_queryset(self):
        school_id = self.request.user.school_id

        if self.request.user.is_superuser:
            return ClassRegistration.objects.filter(pk=self.kwargs[self.lookup_url_kwarg])
        return ClassRegistration.objects.filter(
            cclass__course__school_id=school_id,
            pk=self.kwargs[self.lookup_url_kwarg]
        )


class TestResultListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    # Ajustar
    permission_classes = [IsAuthenticated, IsAccountRoleOwnerOrAdmin]

    serializer_class = serializers.TestResultSerializer

    student_url_kwarg = 'student_id'

    def get_queryset(self):
        school_id = self.request.user.school_id
        student_id = self.kwargs['student_id']
        if self.request.user.is_superuser:
            return TestResult.objects.filter(student_id=student_id)
        return TestResult.objects.filter(
            classroom__cclass__course__school_id=school_id,
            student_id=student_id
        )


class TestResultCreateView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    # Ajeitar
    permission_classes = [IsAuthenticated, IsAccountRoleOwnerOrAdmin]

    serializer_class = serializers.TestResultSerializer

    # def get_queryset(self):
    #     if self.request.user.is_superuser:
    #         return TestResult.objects.all()
    #     school_id = self.request.user.school_id
    #     student_id = self.kwargs['student_id']
    #     return TestResult.objects.filter(classroom__cclass__course__school_id=school_id)

    def perform_create(self, serializer):
        school_id = self.request.user.school_id
        test_id = self.request.data.get('test_id')
        student_id = self.request.data.get('student_id')

        find_student = Account.objects.filter(
            school_id=school_id,
            student_id=student_id,
            role='Student',
        ).first()
        if not find_student:
            raise NotFound("Student not found")

        find_test = Test.objects.filter(
            pk=test_id,
            classroom__cclass__course__school_id=school_id
        ).first()
        if not find_test:
            raise NotFound("Test not found")

        serializer.save(student_id=student_id, test_id=test_id)


class TestResultDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountRoleOwnerOrAdmin,]

    serializer_class = serializers.TestResultSerializer

    lookup_url_kwarg = "test_result_id"

    def get_queryset(self):
        school_id = self.request.user.school_id

        if self.request.user.is_superuser:
            return TestResult.objects.filter(pk=self.kwargs[self.lookup_url_kwarg])
        return TestResult.objects.filter(classroom__cclass__course__school_id=school_id, pk=self.kwargs[self.lookup_url_kwarg])


class AttendanceListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountRoleOwnerOrAdmin]

    serializer_class = serializers.AttendanceSerializer

    student_url_kwarg = 'student_id'

    def get_queryset(self):
        school_id = self.request.user.school_id
        student_id = self.kwargs['student_id']
        if self.request.user.is_superuser:
            return Attendance.objects.filter(student_id=student_id)
        return Attendance.objects.filter(
            occurrence__classroom__cclass__course__school_id=school_id,
            student_id=student_id
        )


class AttendanceCreateView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountRoleOwnerOrAdmin]

    queryset = Attendance.objects.all()
    serializer_class = serializers.AttendanceSerializer

    # def get_queryset(self):
    #     student_id = self.kwargs['student_id']
    #     return Attendance.objects.filter(student__school_id=school_id)

    def perform_create(self, serializer):
        school_id = self.request.user.school_id
        occurrence_id = self.request.data.get('occurrence_id')
        student_id = self.request.data.get('student_id')

        find_student = Account.objects.filter(
            school_id=school_id,
            student_id=student_id,
            role='Student'
        ).first()
        if not find_student:
            raise NotFound("Student not found")

        find_occurrence = Occurrence.objects.filter(
            pk=occurrence_id,
            cclass__course__school_id=school_id
        ).first()
        if not find_occurrence:
            raise NotFound("Occurrence not found")

        serializer.save(student_id=student_id, occurrence_id=classroom_id)


class AttendanceDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountRoleOwnerOrAdmin,]

    serializer_class = serializers.AttendanceSerializer

    lookup_url_kwarg = "attendance_id"

    def get_queryset(self):
        school_id = self.request.user.school_id

        if self.request.user.is_superuser:
            return Attendance.objects.filter(pk=self.kwargs[self.lookup_url_kwarg])
        return Attendance.objects.filter(
            occurrence__classroom__cclass__course__school_id=school_id,
            pk=self.kwargs[self.lookup_url_kwarg]
        )
