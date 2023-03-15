from rest_framework import serializers
from .models import Classroom


class ClassroomSerializer(serializers.ModelSerializer):

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
        }
