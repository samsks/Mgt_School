from rest_framework import serializers
from .models import Account
from django.contrib.auth.hashers import make_password
from utils.choice_classes import AccountRoleOptions
from utils.function_account import generate_unique_uuid, generate_student_code


# Listar todos - precisa listar todos os campos por causa das outras Roles
# Cadastrar Owner - permitir apenas campos do cadastro de Owner e restringir a role para Owner
# Listar account by ID - listar dados de uma account informando id
# Update Owner by ID - atualizar dados de uma account informando seu id
# Delete Owner by ID - deletar conta informando seu id

# OWNER SERIALIZERS
class AccountOwnerSerializer(serializers.ModelSerializer):

    def update(self, instance: Account, validated_data: dict) -> Account:
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
            'password',
            'role',
            'date_joined',
            'last_login',
            'is_staff',
            'is_active',
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
            'school',
        ]
        read_only_fields = [
            'role',
            'date_joined',
            'last_login',
            'updated_at',
            'is_superuser',
            'teacher_id',
            'student_id',
            'school',
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }


class AccountOwnerCreateSerializer(serializers.ModelSerializer):

    def validate_role(self, value):
        if value not in AccountRoleOptions.SCHOOL_OWNER:
            raise serializers.ValidationError("This field must be set to 'Owner'.")
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


# TEACHER SERIALIZERS
class AccountTeacherSerializer(serializers.ModelSerializer):

    def validate_role(self, value):
        if value not in AccountRoleOptions.TEACHER:
            raise serializers.ValidationError("This field must be set to 'Teacher'.")
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

    def update(self, instance: Account, validated_data: dict) -> Account:
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


class AccountStudentSerializer(serializers.ModelSerializer):
    def create(self, validated_data: dict) -> Account:
        return Account.objects.create_user(**validated_data)

    def update(self, instance: Account, validated_data: dict) -> Account:
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
            'password',
            'role',
            'date_joined',
            'last_login',
            'is_staff',
            'is_active',
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
        # extra_kwargs = {
        #     "password": {"write_only": True},
        # }