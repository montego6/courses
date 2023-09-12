# Generated by Django 4.2.2 on 2023-09-12 20:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("courses", "0018_remove_stripecourse_price"),
    ]

    operations = [
        migrations.CreateModel(
            name="TestCompletion",
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
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="test_completions",
                        to="courses.course",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="test_completions",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "test",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="test_completions",
                        to="courses.test",
                    ),
                ),
            ],
        ),
    ]