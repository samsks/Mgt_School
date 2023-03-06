from django.db import models


class School(models.Model):
    company_name = models.CharField(
        max_length=127,
        unique=True,
        error_messages={"unique": "This field must be unique."}
    )
    cnpj = models.BigIntegerField(
        unique=True,
        error_messages={"unique": "This field must be unique."}
    )
    school_phone = models.IntegerField()

    account = models.ForeignKey(
        'accounts.Account',
        on_delete=models.CASCADE,
        related_name='schools',
    )
