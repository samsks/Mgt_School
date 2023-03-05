from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True)
    duration = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField(null=True)

    school = models.ForeignKey(
        'schools.School',
        on_delete=models.CASCADE,
        related_name='courses',
    )
