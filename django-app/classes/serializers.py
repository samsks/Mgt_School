from rest_framework import serializers
from .models import Class
from utils.choice_messages import choices_error_message
from utils.choice_classes import PeriodOptions, ModalityOptions


class ClassSerializer(serializers.ModelSerializer):

    def update(self, instance: Class, validated_data: dict) -> Class:

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
        model = Class
        fields = [
            'id',
            'name',
            'description',
            'period',
            'modality',
            'is_active',
            'course_id',
        ]
        read_only_fields = []
        extra_kwargs = {
            "period": {"error_messages": {"invalid_choice": choices_error_message(PeriodOptions)}},
            "modality": {"error_messages": {"invalid_choice": choices_error_message(ModalityOptions)}},
        }
