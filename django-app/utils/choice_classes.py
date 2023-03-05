from django.db import models


class OfficeOptions(models.TextChoices):
    ACCOUNT_OWNER = 'Account_Owner'
    TEACHER = 'Teacher'


class GenderOptions(models.TextChoices):
    MALE = 'Male'
    FEMALE = 'Female'
    NOT_INFORMED = 'Not Informed'


class PeriodOptions(models.TextChoices):
    MORNING = 'Morning'
    AFTERNOON = 'Afternoon'
    NIGHT = 'Night'
    NOT_INFORMED = 'Not Informed'


class CategoryTestOptions(models.TextChoices):
    FSTQUARTER = '1st Quarter'
    SNDQUARTER = '2nd Quarter'
    TRDQUARTER = '3rd Quarter'
    FTHQUARTER = '4th Quarter'
    FSTRECOVERY = '1st Recovery'
    SNDRECOVERY = '2nd Recovery'
