# Generated by Django 4.2.2 on 2023-08-14 19:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0016_course_is_free_course_subject"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="price",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
