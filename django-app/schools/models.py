from django.db import models


class School(models.Model):
    school_name = models.CharField(max_length=127)
    cnpj = models.BigIntegerField(
        unique=True,
        error_messages={"unique": "This field must be unique."}
    )
    school_phone = models.BigIntegerField(null=True)
    code = models.CharField(
        max_length=50,
        unique=True,
        error_messages={"unique": "This code field must be unique."}
    )
    is_active = models.BooleanField(default=True)
