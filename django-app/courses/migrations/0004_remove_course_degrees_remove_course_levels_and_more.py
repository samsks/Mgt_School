# Generated by Django 4.1.7 on 2023-03-15 07:34

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0003_alter_course_degrees_alter_course_levels_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="course",
            name="degrees",
        ),
        migrations.RemoveField(
            model_name="course",
            name="levels",
        ),
        migrations.RemoveField(
            model_name="course",
            name="themes",
        ),
    ]
