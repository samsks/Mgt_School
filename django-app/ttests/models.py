from django.db import models
from utils.choice_classes import CategoryTestOptions


class Test(models.Model):
    category = models.CharField(
        max_length=12,
        choices=CategoryTestOptions.choices
    )
    test_date = models.DateTimeField()
    max_score = models.DecimalField(max_digits=5, decimal_places=2, default=10)

    classroom = models.ForeignKey(
        'classrooms.Classroom',
        on_delete=models.CASCADE,
        related_name='tests',
    )
