from rest_framework import serializers
from .models import Classroom
from utils.choice_messages import choices_error_message
from utils.choice_classes import RepeatModeOptions


class ClassroomSerializer(serializers.ModelSerializer):

    def update(self, instance: Classroom, validated_data: dict) -> Classroom:

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
        model = Classroom
        fields = [
            'id',
            'matter_name',
            'start_date',
            'end_date',
            'repeat_mode',
            'class_id',
            'teacher_id',
        ]
        extra_kwargs = {
            'class_id': {'source': 'cclass_id'},
            "repeat_mode": {"error_messages": {"invalid_choice": choices_error_message(RepeatModeOptions)}},
        }


class ClassroomCreateSerializer(serializers.ModelSerializer):
    teacher_id = serializers.UUIDField(required=True)
    class_id = serializers.IntegerField(required=True, source="cclass_id")

    class Meta:
        model = Classroom
        fields = [
            'id',
            'matter_name',
            'start_date',
            'end_date',
            'repeat_mode',
            'class_id',
            'teacher_id',
        ]
        extra_kwargs = {
            "repeat_mode": {"error_messages": {"invalid_choice": choices_error_message(RepeatModeOptions)}},
        }
        # extra_kwargs = {
        #     'class_id': {'source': 'cclass_id'},
        # }
