from django.db import models
from django.contrib.auth.models import AbstractUser


class Account(AbstractUser):
    email = models.EmailField(max_length=127, unique=True, error_messages={"unique": "This field must be unique."})
