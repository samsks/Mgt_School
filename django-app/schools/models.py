from django.db import models


class School(models.Model):
    school_name = models.CharField(
        max_length=127,
        # unique=True,
        # error_messages={"unique": "This field must be unique."}
    )
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

    # account = models.ForeignKey(
    #     'accounts.Account',
    #     on_delete=models.CASCADE,
    #     related_name='schools',
    # )
