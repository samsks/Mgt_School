from django.db import models


class Classroom(models.Model):
    matter_name = models.CharField(max_length=50)
    weekdays = models.CharField(max_length=13, default="2,3,4,5,6")

    _class = models.ForeignKey(
        'classes.Class',
        on_delete=models.CASCADE,
        related_name='classrooms',
    )
