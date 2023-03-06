from rest_framework import serializers
from .models import Test
from utils.choice_messages import choices_error_message
from utils.choice_classes import CategoryTestOptions


class TestSerializer(serializers.ModelSerializer):

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
