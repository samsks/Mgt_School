from django.db import models
from utils.choice_classes import GenderOptions
import random
from datetime import datetime
from classes.models import Class
from ttests.models import Test
from classrooms.models import Classroom


def generate_register_number():
    now = datetime.now()
    random_number = random.randint(100000, 999999)

    return f"{now.year}{now.month:02d}{now.day:02d}{random_number}"


class Student(models.Model):
    full_name = models.CharField(max_length=255)
    cpf = models.IntegerField()
    gender = models.CharField(
        max_length=50,
        choices=GenderOptions.choices,
        default=GenderOptions.NOT_INFORMED,
    )
    birthdate = models.DateField()
    phone = models.IntegerField()
    email = models.EmailField(
        max_length=127,
        unique=True,
        error_messages={"unique": "This field must be unique."}
    )
    photo = models.CharField(max_length=255, null=True)
    register_number = models.CharField(max_length=20, default=generate_register_number)
    is_active = models.BooleanField(default=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    school = models.ForeignKey(
        'schools.School',
        on_delete=models.CASCADE,
        related_name='students',
    )

    classes = models.ManyToManyField(
        Class,
        through="ClassRegistration",
        related_name="students"
    )

    ttests = models.ManyToManyField(
        Test,
        through="TestResult",
        related_name="students"
    )

    classrooms = models.ManyToManyField(
        Classroom,
        through="Attendance",
        related_name="students"
    )


class ClassRegistration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    cclass = models.ForeignKey(Class, on_delete=models.CASCADE)

    registered_at = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'students_class_registration'


class TestResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)

    test_grade = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'students_test_result'


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

    showed_up = models.BooleanField(default=False)
    register_date = models.DateTimeField(auto_now=True)
