from django.db import models
from django.core.exceptions import ValidationError
from utils.choice_classes import RepeatModeOptions


class Classroom(models.Model):
    matter_name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    repeat_mode = models.CharField(
        max_length=10,
        choices=RepeatModeOptions.choices,
        default=RepeatModeOptions.WEEKLY,
    )
    is_active = models.BooleanField(default=True)

    def clean(self):
        if self.teacher is not None and self.teacher.role != "Teacher":
            raise ValidationError({"message": "A teacher must be selected."})

    cclass = models.ForeignKey(
        "classes.Class",
        on_delete=models.CASCADE,
        related_name="classrooms",
        # db_column='class_id'
    )

    teacher = models.ForeignKey(
        "accounts.Account",
        to_field="teacher_id",
        on_delete=models.SET_NULL,
        related_name="classrooms",
        limit_choices_to={"role": "Teacher"},
        null=True,
    )
