# Generated by Django 4.1.7 on 2023-03-03 06:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("schools", "0003_rename_phone_number_school_school_phone"),
    ]

    operations = [
        migrations.AlterField(
            model_name="school",
            name="school_phone",
            field=models.BigIntegerField(),
        ),
    ]