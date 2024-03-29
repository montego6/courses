# Generated by Django 4.2.7 on 2024-01-11 21:11

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("courses", "0021_remove_homework_section_remove_lesson_section_and_more"),
        ("contenttypes", "0002_remove_content_type_name"),
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
                ("question", models.CharField(max_length=180)),
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
                        to="sectionitems.test",
                    ),
                ),
            ],
        ),
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
                ("result", models.PositiveIntegerField()),
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
                        to="sectionitems.test",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SectionItem",
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
                ("object_id", models.PositiveIntegerField()),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "section",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="courses.section",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Lesson",
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
                ("file", models.FileField(upload_to="media/courses/lessons/")),
                ("duration", models.PositiveIntegerField(null=True)),
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
                    "section",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="lessons",
                        to="courses.section",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Homework",
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
                ("task", models.CharField(max_length=1000)),
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
                    "section",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="homeworks",
                        to="courses.section",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="AdditionalFile",
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
                ("file", models.FileField(upload_to="media/courses/extra_files/")),
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
                    "section",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="extra_files",
                        to="courses.section",
                    ),
                ),
            ],
        ),
    ]
