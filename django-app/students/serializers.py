from rest_framework import serializers
from .models import Student
from utils.choice_messages import choices_error_message
from utils.choice_classes import GenderOptions


# Voltar aqui ao conf classes
class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = [
            'id',
            'full_name',
            'cpf',
            'gender',
            'birthdate',
            'phone',
            'email',
            'photo',
            "register_number",
            'is_active',
            'registered_at',
            'updated_at',
            'school_id',
            # 'class_id',
        ]
        read_only_fields = ["register_number", 'registered_at', 'updated_at', 'fired_at', 'school_id']
        extra_kwargs = {
            "gender": {"error_messages": {"invalid_choice": choices_error_message(GenderOptions)}},
        }
