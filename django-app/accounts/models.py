from django.db import models
from django.contrib.auth.models import AbstractUser


class OfficeOptions(models.TextChoices):
    ACCOUNT_OWNER = 'Account_Owner'
    TEACHER = 'Teacher'


class Account(AbstractUser):
    email = models.EmailField(
        max_length=127,
        unique=True,
        error_messages={"unique": "This field must be unique."}
    )
    full_name = models.CharField(max_length=255)
    birthdate = models.DateField()
    cpf = models.IntegerField()
    phone = models.IntegerField()
    office = models.CharField(
        max_length=50,
        choices=OfficeOptions.choices,
        default=OfficeOptions.ACCOUNT_OWNER,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
