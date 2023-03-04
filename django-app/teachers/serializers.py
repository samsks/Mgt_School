from rest_framework import serializers
from .models import Teacher
from utils.choice_messages import choices_error_message
from utils.choice_classes import GenderOptions


class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = [
            'id',
            'full_name',
            'cpf',
            'gender',
            'birthdate',
            'phone',
            'email',
            'photo',
            'is_active',
            'registered_at',
            'updated_at',
            'fired_at',
            'school_id',
        ]
        read_only_fields = ['registered_at', 'updated_at', 'fired_at', 'school_id']
        extra_kwargs = {
            "gender": {"error_messages": {"invalid_choice": choices_error_message(GenderOptions)}},
        }
