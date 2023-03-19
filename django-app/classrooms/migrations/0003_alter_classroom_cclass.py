# Generated by Django 4.1.7 on 2023-03-19 02:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("classes", "0001_initial"),
        ("classrooms", "0002_classroom_is_active"),
    ]

    operations = [
        migrations.AlterField(
            model_name="classroom",
            name="cclass",
            field=models.ForeignKey(
                db_column="class_id",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="classrooms",
                to="classes.class",
            ),
        ),
    ]
