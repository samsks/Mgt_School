from rest_framework import serializers
from .models import Classroom
from rest_framework.exceptions import ValidationError
from utils.choice_messages import choices_error_message
from utils.choice_classes import RepeatModeOptions
import copy


class ClassroomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Classroom
        fields = [
            'id',
            'matter_name',
            'start_date',
            'end_date',
            'repeat_mode',
            'is_active',
            'class_id',
            'teacher_id',
        ]
        extra_kwargs = {
            'class_id': {'source': 'cclass_id'},
            "repeat_mode": {"error_messages": {"invalid_choice": choices_error_message(RepeatModeOptions)}},
        }


class ClassroomCreateSerializer(serializers.ModelSerializer):
    # teacher_id = serializers.UUIDField(allow_null=True)
    class_id = serializers.IntegerField(required=True, source="cclass_id")

    def update(self, instance: Classroom, validated_data: dict) -> Classroom:

        valid_data = copy.deepcopy(validated_data)
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
            'is_active',
            'class_id',
            'teacher_id',
        ]
        # read_only = ['is_active',]
        extra_kwargs = {
            "repeat_mode": {"error_messages": {"invalid_choice": choices_error_message(RepeatModeOptions)}},
        }
        # extra_kwargs = {
        #     'class_id': {'source': 'cclass_id'},
        # }
