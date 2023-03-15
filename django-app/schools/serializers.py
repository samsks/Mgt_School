from rest_framework import serializers
from .models import School


class SchoolSerializer(serializers.ModelSerializer):

    def update(self, instance: School, validated_data: dict) -> School:

        valid_data = validated_data.copy()
        for attr, value in validated_data.items():
            if getattr(instance, attr) == value:
                print(attr)
                valid_data.pop(attr)

        if not valid_data:
            raise ValidationError({'message': 'There are no changes to be saved.'})

        for key, value in valid_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

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


class SchoolOnlyInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = ['id', 'school_name', 'school_phone',]
        read_only_fields = ['school_name', 'cnpj', 'school_phone', 'code']
