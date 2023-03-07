from rest_framework import serializers
from .models import Classroom


class ClassroomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Classroom
        fields = [
            'id',
            'matter_name',
            'weekdays',
            'class_id',
        ]
        extra_kwargs = {
            'class_id': {'source': 'cclass_id'},
        }
