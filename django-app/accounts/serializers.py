from rest_framework import serializers
from .models import Account, ClassRegistration, TestResult, Attendance
from django.contrib.auth.hashers import make_password
from utils.choice_classes import AccountRoleOptions
from utils.choice_messages import choices_error_message
from utils.function_account import generate_unique_uuid, generate_student_code
from rest_framework.exceptions import ValidationError


# Listar todos - precisa listar todos os campos por causa das outras Roles
# Cadastrar Owner - permitir apenas campos do cadastro de Owner e restringir a role para Owner
# Listar account by ID - listar dados de uma account informando id
# Update Owner by ID - atualizar dados de uma account informando seu id
# Delete Owner by ID - deletar conta informando seu id

# OWNER SERIALIZERS
class AccountOwnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = [
            'id',
            'username',
            'password',
            'role',
            'date_joined',
            'last_login',
            'is_staff',
            'is_active',
            'school_id',
            # relations with address and school
            'cpf',
            'first_name',
            'middle_name',
            'last_name',
            'email',
            'birthdate',
            'phone',
            'photo',
            'bio',
            'updated_at',
            'teacher_id',
            'major',
            'fired_at',
            'fired_reason',
            'student_id',
            'student_code',
        ]
        read_only_fields = [
            'role',
            'date_joined',
            'last_login',
            'updated_at',
            'is_superuser',
            'teacher_id',
            'student_id',
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }


class AccountOwnerCreateSerializer(serializers.ModelSerializer):

    def validate_role(self, value):
        if value not in AccountRoleOptions.SCHOOL_OWNER:
            raise serializers.ValidationError({'message': "This field must be set to 'Owner'."})
        return value

    def create(self, validated_data: dict) -> Account:

        return Account.objects.create_user(
            **validated_data,
            role='Owner',
        )

    class Meta:
        model = Account
        fields = [
            'id',
            'username',
            'password',
            'role',
            'date_joined',
            'last_login',
            'is_staff',
            'is_active',
            'school_id',
            # relations with address and school
            'cpf',
            'first_name',
            'middle_name',
            'last_name',
            'email',
            'birthdate',
            'phone',
            'photo',
            'bio',
            'updated_at',
        ]
        read_only_fields = [
            'role',
            'date_joined',
            'last_login',
            'updated_at',
            'is_superuser',
            'school_id',
            'teacher_id',
            'major',
            'fired_at',
            'fired_reason',
            'student_id',
            'student_code',
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }


class AccountOwnerDetailSerializer(serializers.ModelSerializer):

    def update(self, instance: Account, validated_data: dict) -> Account:

        valid_data = validated_data.copy()
        for attr, value in validated_data.items():
            if getattr(instance, attr) == value:
                print(attr)
                valid_data.pop(attr)

        if not valid_data:
            raise ValidationError({'message': 'There are no changes to be saved.'})

        for key, value in valid_data.items():
            if key == "password":
                instance.set_password(value)
                continue
            setattr(instance, key, value)

        instance.save()

        return instance

    class Meta:
        model = Account
        fields = [
            'id',
            'username',
            'password',
            'role',
            'date_joined',
            'last_login',
            'is_staff',
            'is_active',
            'school_id',
            'cpf',
            'first_name',
            'middle_name',
            'last_name',
            'email',
            'birthdate',
            'phone',
            'photo',
            'bio',
            'updated_at',
            'teacher_id',
            'major',
            'fired_at',
            'fired_reason',
            'student_id',
            'student_code',
        ]
        read_only_fields = [
            'date_joined',
            'last_login',
            'updated_at',
            'is_superuser',
            'teacher_id',
            'student_id',
            'student_code',
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "role": {"error_messages": {"invalid_choice": choices_error_message(AccountRoleOptions)}},
        }


# TEACHER SERIALIZERS
class AccountTeacherListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = [
            'id',
            'role',
            'is_active',
            'first_name',
            'last_name',
            'email',
            'birthdate',
            'phone',
            'photo',
            'bio',
            'major',
        ]
        read_only_fields = [
            'role',
            'date_joined',
            'last_login',
            'is_staff',
            'updated_at',
            'is_superuser',
            'is_active',
            'school_id',
            'teacher_id',
            'fired_at',
            'fired_reason',
            'student_id',
            'student_code',
        ]


class AccountTeacherCreateSerializer(serializers.ModelSerializer):

    def validate_role(self, value):
        if value not in AccountRoleOptions.TEACHER:
            raise serializers.ValidationError({'message': "This field must be set to 'Teacher'."})
        return value

    def create(self, validated_data: dict) -> Account:
        user = self.context['request'].user
        validated_data['school_id'] = user.school_id

        cpf = str(validated_data.get("cpf"))
        last_name = validated_data.get("last_name")

        return Account.objects.create_user(
            **validated_data,
            username=str(cpf),
            password=f"{cpf[:4]}@{last_name}",
            role='Teacher',
            teacher_id=generate_unique_uuid(Account, 'teacher_id'),
        )

    class Meta:
        model = Account
        fields = [
            'id',
            'username',
            'role',
            'date_joined',
            'last_login',
            'is_staff',
            'is_active',
            'school_id',
            # relations with address and school
            'cpf',
            'first_name',
            'middle_name',
            'last_name',
            'email',
            'birthdate',
            'phone',
            'photo',
            'bio',
            'updated_at',
            'teacher_id',
            'major',
            'fired_at',
            'fired_reason',
        ]
        read_only_fields = [
            'username',
            'role',
            'date_joined',
            'last_login',
            'is_staff',
            'updated_at',
            'is_superuser',
            'teacher_id',
            'fired_at',
            'fired_reason',
            'student_id',
            'student_code',
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }


class AccountTeacherUpdateSerializer(serializers.ModelSerializer):

    def validate_role(self, value):
        if value not in AccountRoleOptions.TEACHER:
            raise serializers.ValidationError({'message': "This field must be set to 'Teacher'."})
        return value

    def update(self, instance: Account, validated_data: dict) -> Account:
        valid_data = validated_data.copy()
        for attr, value in validated_data.items():
            if getattr(instance, attr) == value:
                print(attr)
                valid_data.pop(attr)

        if not valid_data:
            raise ValidationError({'message': 'There are no changes to be saved.'})

        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
                continue
            setattr(instance, key, value)

        instance.save()

        return instance

    class Meta:
        model = Account
        fields = [
            'id',
            'username',
            'role',
            'date_joined',
            'last_login',
            'is_active',
            'updated_at',
            'school_id',
            'cpf',
            'first_name',
            'middle_name',
            'last_name',
            'email',
            'birthdate',
            'phone',
            'photo',
            'bio',
            'teacher_id',
            'major',
        ]
        read_only_fields = [
            'role',
            'date_joined',
            'last_login',
            'is_staff',
            'is_active',
            'updated_at',
            'is_superuser',
            'schools_id',
            'cpf',
            'first_name',
            'middle_name',
            'last_name',
            'birthdate',
            'teacher_id',
            'fired_at',
            'fired_reason',
            'student_id',
            'student_code',
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }


# STUDENT SERIALIZERS
class AccountStudentSerializer(serializers.ModelSerializer):

    def validate_role(self, value):
        if value not in AccountRoleOptions.STUDENT:
            raise serializers.ValidationError({'message': "This field must be set to 'Student'."})
        return value

    def create(self, validated_data: dict) -> Account:
        user = self.context['request'].user
        validated_data['school_id'] = user.school_id

        cpf = str(validated_data.get("cpf"))
        last_name = validated_data.get("last_name")

        return Account.objects.create_user(
            **validated_data,
            username=str(cpf),
            password=f"{cpf[:4]}@{last_name}",
            role='Student',
            student_id=generate_unique_uuid(Account, 'student_id'),
            student_code=generate_student_code(Account, 'student_code')
        )

    def update(self, instance: Account, validated_data: dict) -> Account:
        valid_data = validated_data.copy()
        for attr, value in validated_data.items():
            if getattr(instance, attr) == value:
                print(attr)
                valid_data.pop(attr)

        if not valid_data:
            raise ValidationError({'message': 'There are no changes to be saved.'})

        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
                continue
            setattr(instance, key, value)

        instance.save()

        return instance

    class Meta:
        model = Account
        fields = [
            'id',
            'username',
            'role',
            'date_joined',
            'last_login',
            'is_staff',
            'is_active',
            'school_id',
            'cpf',
            'first_name',
            'middle_name',
            'last_name',
            'email',
            'birthdate',
            'phone',
            'photo',
            'bio',
            'updated_at',
            'student_id',
            'student_code',

        ]
        read_only_fields = [
            'username',
            'role',
            'date_joined',
            'last_login',
            'is_staff',
            'is_active',
            'updated_at',
            'is_superuser',
            'teacher_id',
            'major',
            'fired_at',
            'fired_reason',
            'student_id',
            'student_code',
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }


class AccountStudentListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = [
            'id',
            'role',
            'is_active',
            'first_name',
            'last_name',
            'email',
            'birthdate',
            'phone',
            'photo',
            'bio',
        ]
        read_only_fields = [
            'role',
            'date_joined',
            'last_login',
            'is_staff',
            'updated_at',
            'is_superuser',
            'is_active',
            'school_id',
            'teacher_id',
            'fired_at',
            'fired_reason',
            'student_id',
            'student_code',
        ]


class AccountStudentCreateSerializer(serializers.ModelSerializer):

    def validate_role(self, value):
        if value not in AccountRoleOptions.STUDENT:
            raise serializers.ValidationError({'message': "This field must be set to 'Student'."})
        return value

    def create(self, validated_data: dict) -> Account:
        user = self.context['request'].user
        validated_data['school_id'] = user.school_id

        cpf = str(validated_data.get("cpf"))
        last_name = validated_data.get("last_name")

        return Account.objects.create_user(
            **validated_data,
            username=str(cpf),
            password=f"{cpf[:4]}@{last_name}",
            role='Student',
            student_id=generate_unique_uuid(Account, 'student_id'),
            student_code=generate_student_code(Account, 'student_code')
        )

    class Meta:
        model = Account
        fields = [
            'id',
            'username',
            'role',
            'date_joined',
            'last_login',
            'is_staff',
            'is_active',
            'school_id',
            'cpf',
            'first_name',
            'middle_name',
            'last_name',
            'email',
            'birthdate',
            'phone',
            'photo',
            'bio',
            'updated_at',
            'student_id',
            'student_code',
        ]
        read_only_fields = [
            'username',
            'role',
            'date_joined',
            'last_login',
            'is_staff',
            'updated_at',
            'is_superuser',
            'teacher_id',
            'major',
            'fired_at',
            'fired_reason',
            'student_id',
            'student_code',
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }


class AccountStudentUpdateSerializer(serializers.ModelSerializer):

    def validate_role(self, value):
        if value not in AccountRoleOptions.STUDENT:
            raise serializers.ValidationError({'message': "This field must be set to 'Student'."})
        return value

    def update(self, instance: Account, validated_data: dict) -> Account:
        valid_data = validated_data.copy()
        for attr, value in validated_data.items():
            if getattr(instance, attr) == value:
                print(attr)
                valid_data.pop(attr)

        if not valid_data:
            raise ValidationError({'message': 'There are no changes to be saved.'})

        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
                continue
            setattr(instance, key, value)

        instance.save()

        return instance

    class Meta:
        model = Account
        fields = [
            'id',
            'username',
            'role',
            'date_joined',
            'last_login',
            'is_active',
            'updated_at',
            'school_id',
            'cpf',
            'first_name',
            'middle_name',
            'last_name',
            'email',
            'birthdate',
            'phone',
            'photo',
            'bio',
            'student_id',
            'student_code',
        ]
        read_only_fields = [
            'role',
            'date_joined',
            'last_login',
            'is_staff',
            'is_active',
            'updated_at',
            'is_superuser',
            'schools_id',
            'cpf',
            'first_name',
            'middle_name',
            'last_name',
            'birthdate',
            'teacher_id',
            'fired_at',
            'fired_reason',
            'student_id',
            'student_code',
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }


# PIVOT TABLES SERIALIZERS WITH STUDENT

class ClassRegistrationSerializer(serializers.ModelSerializer):

    def update(self, instance: ClassRegistration, validated_data: dict) -> ClassRegistration:

        valid_data = validated_data.copy()
        for attr, value in validated_data.items():
            if getattr(instance, attr) == value:
                valid_data.pop(attr)

        if not valid_data:
            raise ValidationError({'message': 'There are no changes to be saved.'})

        for key, value in valid_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

    class Meta:
        model = ClassRegistration
        fields = [
            'id',
            'registered_at',
            'updated_at',
            'is_active',
            'student_id',
            'class_id',
        ]
        read_only_fields = ['registered_at', 'updated_at']
        extra_kwargs = {"class_id": {"source": "cclass_id"}}


class ClassRegistrationCreateSerializer(serializers.ModelSerializer):
    student_id = serializers.UUIDField(required=True)
    class_id = serializers.IntegerField(required=True, source="cclass_id")

    class Meta:
        model = ClassRegistration
        fields = [
            'id',
            'registered_at',
            'updated_at',
            'is_active',
            'student_id',
            'class_id',
        ]
        read_only_fields = ['registered_at', 'updated_at', 'is_active']
        # extra_kwargs = {"class_id": {"source": "cclass_id"}}


class TestResultSerializer(serializers.ModelSerializer):

    def update(self, instance: TestResult, validated_data: dict) -> TestResult:

        valid_data = validated_data.copy()
        for attr, value in validated_data.items():
            if getattr(instance, attr) == value:
                valid_data.pop(attr)

        if not valid_data:
            raise ValidationError({'message': 'There are no changes to be saved.'})

        for key, value in valid_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

    class Meta:
        model = TestResult
        fields = [
            'id',
            'test_grade',
            'registered_at',
            'updated_at',
            'student_id',
            'test_id',
        ]
        read_only_fields = ['registered_at', 'updated_at']


class AttendanceSerializer(serializers.ModelSerializer):

    def update(self, instance: Attendance, validated_data: dict) -> Attendance:

        valid_data = validated_data.copy()
        for attr, value in validated_data.items():
            if getattr(instance, attr) == value:
                valid_data.pop(attr)

        if not valid_data:
            raise ValidationError({'message': 'There are no changes to be saved.'})

        for key, value in valid_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

    class Meta:
        model = Attendance
        fields = [
            'id',
            'showed_up',
            'register_date',
            'updated_at',
            'occurrence_id',
            'student_id',
        ]
