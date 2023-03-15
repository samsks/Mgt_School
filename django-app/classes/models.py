from django.db import models
from utils.choice_classes import PeriodOptions, ModalityOptions


class Class(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True)
    # duration = models.CharField(max_length=20, null=True)
    period = models.CharField(
        max_length=10,
        choices=PeriodOptions.choices,
    )
    modality = models.CharField(
        max_length=6,
        choices=ModalityOptions.choices,
    )
    # hour = models.TimeField()
    is_active = models.BooleanField(default=True)

    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.PROTECT,
        related_name='classes',
    )

    # teacher = models.ForeignKey(
    #     'teachers.Teacher',
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     related_name='classes',
    # )
