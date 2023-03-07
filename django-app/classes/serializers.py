from rest_framework import serializers
from .models import Class
from utils.choice_messages import choices_error_message
from utils.choice_classes import PeriodOptions


class ClassSerializer(serializers.ModelSerializer):

    class Meta:
        model = Class
        fields = [
            'id',
            'name',
            'description',
            'duration',
            'period',
            'hour',
            'course_id',
            'teacher_id',
        ]
        read_only_fields = []
        extra_kwargs = {
            "period": {"error_messages": {"invalid_choice": choices_error_message(PeriodOptions)}},
        }
