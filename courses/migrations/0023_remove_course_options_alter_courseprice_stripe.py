# Generated by Django 4.2.7 on 2024-01-17 18:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0022_remove_course_price_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="course",
            name="options",
        ),
        migrations.AlterField(
            model_name="courseprice",
            name="stripe",
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
