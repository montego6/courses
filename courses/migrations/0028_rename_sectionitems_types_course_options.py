# Generated by Django 4.2.7 on 2024-03-18 16:02

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0027_course_sectionitems_types"),
    ]

    operations = [
        migrations.RenameField(
            model_name="course",
            old_name="sectionitems_types",
            new_name="options",
        ),
    ]