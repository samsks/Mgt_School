from rest_framework import serializers
from .models import School


class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = ['id', 'company_name', 'cnpj', 'school_phone', 'account_id']
        read_only_fields = ["account_id"]
