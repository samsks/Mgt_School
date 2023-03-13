from django.db import models
from django.contrib.auth.models import AbstractUser
from utils.choice_classes import AccountRoleOptions
import uuid


class Account(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=AccountRoleOptions.choices,
    )

    # COMMON DETAILS - FOR ROLES: OWNER, TEACHER AND STUDENT
    cpf = models.BigIntegerField(
        unique=True,
        error_messages={"unique": "This C.P.F field must be unique."},
        # need REGEX
    )
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=128, null=True)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(
        max_length=127,
        unique=True,
        error_messages={"unique": "This email field must be unique."}
    )
    birthdate = models.DateField(
        null=True
        # need REGEX
    )
    phone = models.BigIntegerField(
        null=True
        # need REGEX
    )
    photo = models.CharField(max_length=255, null=True)
    bio = models.TextField(null=True)
    updated_at = models.DateTimeField(auto_now=True)

    # TEACHER DETAILS - ONLY FOR ROLE: TEACHER
    teacher_id = models.UUIDField(unique=True, editable=False, null=True)
    major = models.CharField(max_length=50, null=True)
    fired_at = models.DateField(null=True)
    fired_reason = models.CharField(max_length=255, null=True)

    # STUDENT DETAILS - ONLY FOR ROLE: STUDENT
    student_id = models.UUIDField(unique=True, editable=False, null=True)
    student_code = models.CharField(max_length=20, editable=False, unique=True, null=True)

    school = models.ForeignKey(
        'schools.School',
        on_delete=models.SET_NULL,
        related_name='accounts',
        null=True
    )
