from rest_framework import serializers
from .models import Classroom


# Voltar aqui ao conf classes
class ClassroomSerializer(serializers.ModelSerializer):
    course_id = serializers.IntegerField(write_only=True)
    # class_id = serializers.IntegerField(required=True, source='_class_id')

    class Meta:
        model = Classroom
        fields = [
            'id',
            'matter_name',
            'weekdays',
            'class_id',
            'course_id',
        ]
        extra_kwargs = {
            'class_id': {'source': 'cclass_id'},
            # 'course_id': {"write_only": True},
        }

    def create(self, validated_data):
        course_id = validated_data.pop('course_id')
        classroom = Classroom.objects.create(**validated_data)
        return classroom
