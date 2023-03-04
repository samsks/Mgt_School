from django.db import models
from utils.choice_classes import GenderOptions
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone


class Teacher(models.Model):
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
    is_active = models.BooleanField(default=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    fired_at = models.DateTimeField(blank=True, null=True)

    school = models.ForeignKey(
        'schools.School',
        on_delete=models.CASCADE,
        related_name='teachers',
    )


# testar
@receiver(pre_save, sender=Teacher)
def set_fired_at(sender, instance, **kwargs):
    if not instance.is_active and not instance.fired_at:
        instance.fired_at = timezone.now()
