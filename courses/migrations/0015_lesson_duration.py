# Generated by Django 4.2.2 on 2023-07-26 14:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0014_stripecourse_option_prices"),
    ]

    operations = [
        migrations.AddField(
            model_name="lesson",
            name="duration",
            field=models.PositiveIntegerField(null=True),
        ),
    ]
