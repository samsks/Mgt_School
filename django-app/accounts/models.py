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


# PIVOT TABLES ONLY FOR ROLE STUDENT

class ClassRegistration(models.Model):
    student = models.ForeignKey(
        Account,
        to_field='student_id',
        on_delete=models.CASCADE,
        related_name='class_registration',
        limit_choices_to={'role': 'Student'},
    )
    cclass = models.ForeignKey(
        'classes.Class',
        on_delete=models.CASCADE,
        related_name='class_registration'
    )

    registered_at = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def clean(self):
        if self.teacher is not None and self.teacher.role != 'Student':
            raise ValidationError({'message': 'A student must be selected.'})

    class Meta:
        db_table = 'students_class_registration'


class TestResult(models.Model):
    student = models.ForeignKey(
        Account,
        to_field='student_id',
        on_delete=models.CASCADE,
        related_name='test_results',
        limit_choices_to={'role': 'Student'},
    )
    test = models.ForeignKey(
        'ttests.Test',
        on_delete=models.CASCADE,
        related_name='test_results',
    )

    test_grade = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'students_test_results'


class Attendance(models.Model):
    student = models.ForeignKey(
        Account,
        to_field='student_id',
        on_delete=models.CASCADE,
        related_name='attendance',
        limit_choices_to={'role': 'Student'},
    )
    occurrence = models.ForeignKey(
        'occurrences.Occurrence',
        on_delete=models.CASCADE,
        related_name='attendance',
    )

    showed_up = models.BooleanField(default=False)
    register_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
