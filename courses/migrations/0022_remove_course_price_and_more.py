# Generated by Django 4.2.7 on 2024-01-17 17:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0021_remove_homework_section_remove_lesson_section_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="course",
            name="price",
        ),
        migrations.RemoveField(
            model_name="stripecourse",
            name="option_prices",
        ),
        migrations.CreateModel(
            name="CourseUpgradePrice",
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
                ("amount", models.PositiveIntegerField()),
                ("stripe", models.CharField(max_length=64)),
                ("stripe_product", models.CharField(max_length=64)),
                (
                    "from_option",
                    models.CharField(
                        choices=[
                            ("basic", "All the basic content"),
                            ("extra", "Some additional files"),
                        ],
                        default="basic",
                        max_length=20,
                    ),
                ),
                (
                    "to_option",
                    models.CharField(
                        choices=[
                            ("extra", "Some additional files"),
                            ("premium", "All the content you need"),
                        ],
                        default="extra",
                        max_length=20,
                    ),
                ),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="upgrades",
                        to="courses.course",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CoursePrice",
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
                ("amount", models.PositiveIntegerField()),
                ("stripe", models.CharField(max_length=64)),
                (
                    "option",
                    models.CharField(
                        choices=[
                            ("free", "It is a free content"),
                            ("basic", "All the basic content"),
                            ("extra", "Some additional files"),
                            ("premium", "All the content you need"),
                        ],
                        default="basic",
                        max_length=20,
                    ),
                ),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="prices",
                        to="courses.course",
                    ),
                ),
            ],
        ),
    ]
