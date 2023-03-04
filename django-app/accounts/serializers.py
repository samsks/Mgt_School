from rest_framework import serializers
from .models import Account, OfficeOptions

from django.contrib.auth.hashers import make_password


# Removi pois sem necessidade em account. Reaproveitar em outros choices

# def choices_error_message(choices_class):
#     valid_choices = [choice[0] for choice in choices_class.choices]
#     message = ", ".join(valid_choices).rsplit(",", 1)

#     return "Choose between " + " and".join(message) + "."


class AccountSerializer(serializers.ModelSerializer):

    # def validate_password(self, value):
    #     return make_password(value)

    def create(self, validated_data: dict) -> Account:
        return Account.objects.create_user(**validated_data)

    def update(self, instance: Account, validated_data: dict) -> Account:
        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
                continue
            setattr(instance, key, value)

        instance.save()

        return instance

    class Meta:
        model = Account
        fields = [
            'id',
            'password',
            'username',
            'email',
            'full_name',
            'cpf',
            'birthdate',
            'phone',
            'office',
            'is_staff',
            'is_active',
            'date_joined',
            'last_login',
        ]
        read_only_fields = ['office', 'is_staff', 'is_active', 'date_joined', 'last_login', 'is_superuser']
        extra_kwargs = {
            "password": {"write_only": True},
            # "office": {"error_messages": {"invalid_choice": choices_error_message(OfficeOptions)}},
        }
