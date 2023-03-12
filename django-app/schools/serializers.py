from rest_framework import serializers
from .models import School


class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = ['id', 'school_name', 'cnpj', 'school_phone', 'code']
        # read_only_fields = []

    # def create(self, validated_data):
    #     school = School.objects.create(**validated_data)

    #     user = self.context['request'].user
    #     user.school = school
    #     user.save()

    #     return school
