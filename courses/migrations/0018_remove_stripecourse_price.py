# Generated by Django 4.2.2 on 2023-09-11 21:12

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0017_alter_course_price"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="stripecourse",
            name="price",
        ),
    ]
