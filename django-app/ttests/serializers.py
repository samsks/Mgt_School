from rest_framework import serializers
from .models import Test
from utils.choice_messages import choices_error_message
from utils.choice_classes import CategoryTestOptions


class TestSerializer(serializers.ModelSerializer):

    def update(self, instance: Test, validated_data: dict) -> Test:

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
        model = Test
        fields = [
            'id',
            'category',
            'test_date',
            'max_score',
            'classroom_id',
        ]
        extra_kwargs = {
            "category": {"error_messages": {"invalid_choice": choices_error_message(CategoryTestOptions)}},
        }
