import uuid
from django.db import IntegrityError
from datetime import datetime
from accounts.models import Account


def generate_student_code(model, field):
    """
    Generate a unique student_code for Account role Student.
    """
    now = datetime.now()
    occurrence = 0
    while True:
        student_code = f"{now.year}{now.month:02d}{now.day:02d}-{now.hour:02d}{now.minute:02d}{now.minute:02d}.{occurrence:02d}"
        if not model.objects.filter(**{field: student_code}).exists():
            return student_code
        occurrence += 1


def generate_unique_uuid(model, field):
    """
    Generate a unique UUID for Account role Student and Teacher.
    """
    while True:
        uuid_value = uuid.uuid4()
        if not model.objects.filter(**{field: uuid_value}).exists():
            return uuid_value
