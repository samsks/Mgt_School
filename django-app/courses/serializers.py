from rest_framework import serializers
from .models import Course
from utils.choice_classes import ModalityOptions
from utils.choice_messages import choices_error_message
from rest_framework.exceptions import ValidationError


class CourseSerializer(serializers.ModelSerializer):

    def update(self, instance: Course, validated_data: dict) -> Course:

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
        model = Course
        fields = [
            'id',
            'name',
            'modality',
            'description',
            'start_date',
            'end_date',
            'duration_in_weeks',
            'is_active',
            'school_id',
        ]
        read_only_fields = ['school_id']
        extra_kwargs = {
            "modality": {"error_messages": {"invalid_choice": choices_error_message(ModalityOptions)}},
        }
