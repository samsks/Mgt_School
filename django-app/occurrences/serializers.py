from rest_framework import serializers
from .models import Occurrence
from utils.choice_messages import choices_error_message
from utils.choice_classes import WeekdaysOptions


class OccurrenceSerializer(serializers.ModelSerializer):

    def update(self, instance: Occurrence, validated_data: dict) -> Occurrence:

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
        model = Occurrence
        fields = [
            'id',
            'start',
            'end',
            'weekday',
            'date',
            'classroom_id',
        ]
        extra_kwargs = {
            "weekday": {"error_messages": {"invalid_choice": choices_error_message(WeekdaysOptions)}},
        }
