# Generated by Django 4.1.7 on 2023-03-13 00:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("schools", "0009_alter_school_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="school",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]