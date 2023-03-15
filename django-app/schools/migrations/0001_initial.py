# Generated by Django 4.1.7 on 2023-03-15 07:23

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="School",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("school_name", models.CharField(max_length=127)),
                (
                    "cnpj",
                    models.BigIntegerField(
                        error_messages={"unique": "The cnpj field must be unique."},
                        unique=True,
                    ),
                ),
                ("school_phone", models.BigIntegerField(null=True)),
                (
                    "code",
                    models.CharField(
                        error_messages={"unique": "The code field must be unique."},
                        max_length=50,
                        unique=True,
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
            ],
        ),
    ]
