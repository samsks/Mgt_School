from django.db import models


class OfficeOptions(models.TextChoices):
    ACCOUNT_OWNER = 'Account_Owner'
    TEACHER = 'Teacher'


class GenderOptions(models.TextChoices):
    MALE = 'Male'
    FEMALE = 'Female'
    NOT_INFORMED = 'Not Informed'
