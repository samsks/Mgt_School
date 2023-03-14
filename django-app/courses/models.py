from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from utils.choice_classes import ModalityOptions


class Course(models.Model):
    name = models.CharField(max_length=50)
    modality = models.CharField(
        max_length=6,
        choices=ModalityOptions.choices,
    )
    description = models.TextField(null=True)
    duration_in_weeks = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)])
    start_date = models.DateField()
    end_date = models.DateField(null=True)

    school = models.ForeignKey(
        'schools.School',
        on_delete=models.CASCADE,
        related_name='courses',
    )
