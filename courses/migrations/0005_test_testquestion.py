# Generated by Django 4.2.2 on 2023-06-26 14:03

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0004_sectionitem_additionalfile"),
    ]

    operations = [
        migrations.CreateModel(
            name="Test",
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
                ("name", models.CharField(max_length=80)),
                ("description", models.CharField(max_length=200, null=True)),
                (
                    "section",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tests",
                        to="courses.section",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TestQuestion",
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
                (
                    "options",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=100), size=3
                    ),
                ),
                ("answer", models.CharField(max_length=100)),
                (
                    "test",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="questions",
                        to="courses.test",
                    ),
                ),
            ],
        ),
    ]