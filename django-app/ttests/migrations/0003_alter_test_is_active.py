# Generated by Django 4.1.7 on 2023-03-19 02:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ttests", "0002_test_is_active"),
    ]

    operations = [
        migrations.AlterField(
            model_name="test",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]
