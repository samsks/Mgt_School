from rest_framework import serializers
from .models import Course


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = [
            'name',
            'description',
            'duration',
            'start_date',
            'end_date',
            'school_id',
        ]
        read_only_fields = ['school_id']
