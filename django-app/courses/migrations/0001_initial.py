# Generated by Django 4.1.7 on 2023-03-04 22:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("schools", "0007_school_account"),
    ]

    operations = [
        migrations.CreateModel(
            name="Course",
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
                ("name", models.CharField(max_length=50)),
                ("description", models.TextField(null=True)),
                ("duration", models.CharField(max_length=20)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField(null=True)),
                (
                    "school",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="courses",
                        to="schools.school",
                    ),
                ),
            ],
        ),
    ]