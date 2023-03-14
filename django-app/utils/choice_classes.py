from django.db import models


class AccountRoleOptions(models.TextChoices):
    SCHOOL_OWNER = 'Owner'
    TEACHER = 'Teacher'
    STUDENT = 'Student'


class GenderOptions(models.TextChoices):
    MALE = 'Male'
    FEMALE = 'Female'
    NOT_INFORMED = 'Not Informed'


class ModalityOptions(models.TextChoices):
    PERSON = 'Person'
    ONLINE = 'Online'
    HYBRID = 'Hybrid'


class PeriodOptions(models.TextChoices):
    MORNING = 'Morning'
    AFTERNOON = 'Afternoon'
    NIGHT = 'Night'
    CUSTOM = 'Custom'


class CategoryTestOptions(models.TextChoices):
    FSTQUARTER = '1st Quarter'
    SNDQUARTER = '2nd Quarter'
    TRDQUARTER = '3rd Quarter'
    FTHQUARTER = '4th Quarter'
    FSTRECOVERY = '1st Recovery'
    SNDRECOVERY = '2nd Recovery'


class WeekdaysOptions(models.TextChoices):
    SUNDAY = 'Sunday'
    MONDAY = 'Monday'
    TUESDAY = 'Tuesday'
    WEDNESDAY = 'Wednesday'
    THURSDAY = 'Thursday'
    FRIDAY = 'Friday'
    SATURDAY = 'Saturday'


class RepeatModeOptions(models.TextChoices):
    WEEKLY = 'Weekly'
    BIWEEKLY = 'Biweekly'
    MONTHLY = 'Monthly'
    YEARLY = 'Yearly'
