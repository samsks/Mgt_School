from django.db import models
from utils.choice_classes import WeekdaysOptions


class Occurrence(models.Model):
    start = models.TimeField()
    end = models.TimeField()
    weekday = models.CharField(
        max_length=10,
        choices=WeekdaysOptions.choices,
    )
    date = models.DateField()

    classroom = models.ForeignKey(
        'classrooms.Classroom',
        on_delete=models.CASCADE,
        related_name='occurrences',
    )
