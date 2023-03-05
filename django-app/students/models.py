from django.db import models
from utils.choice_classes import GenderOptions
import random
from datetime import datetime


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

    # class = models.ForeignKey(
    #     'teachers.Teacher',
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     related_name='classes',
    # )