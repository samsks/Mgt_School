from rest_framework import serializers
from .models import Test
from utils.choice_messages import choices_error_message
from utils.choice_classes import CategoryTestOptions


class TestSerializer(serializers.ModelSerializer):
    course_id = serializers.IntegerField(write_only=True)
    class_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Test
        fields = [
            'id',
            'category',
            'test_date',
            'max_score',
            'course_id',
            'class_id',
            'classroom_id',
        ]
        extra_kwargs = {
            "category": {"error_messages": {"invalid_choice": choices_error_message(CategoryTestOptions)}},
        }

    def create(self, validated_data):
        course_id = validated_data.pop('course_id')
        class_id = validated_data.pop('class_id')
        test = Test.objects.create(**validated_data)
        return test
