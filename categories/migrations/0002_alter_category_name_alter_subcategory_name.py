# Generated by Django 4.2.2 on 2023-06-20 17:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("categories", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(
                max_length=50,
                unique=True,
                validators=[
                    django.core.validators.MinLengthValidator(
                        5, message="Количество символов должно быть больше 4"
                    ),
                    django.core.validators.RegexValidator(
                        "[А-Яа-я\\-]+", message="Допускаются только кириллические буквы"
                    ),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="subcategory",
            name="name",
            field=models.CharField(
                max_length=50,
                unique=True,
                validators=[
                    django.core.validators.MinLengthValidator(
                        5, message="Количество символов должно быть больше 4"
                    ),
                    django.core.validators.RegexValidator(
                        "[А-Яа-я\\-]+", message="Допускаются только кириллические буквы"
                    ),
                ],
            ),
        ),
    ]