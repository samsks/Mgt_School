from django.db import models
from utils.choice_classes import PeriodOptions


class Class(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True)
    duration = models.CharField(max_length=20, null=True)
    period = models.CharField(
        max_length=20,
        choices=PeriodOptions.choices,
        default=PeriodOptions.NOT_INFORMED,
    )
    hour = models.TimeField()

    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE,
        related_name='classes',
    )

    teacher = models.ForeignKey(
        'teachers.Teacher',
        on_delete=models.SET_NULL,
        null=True,
        related_name='classes',
    )
