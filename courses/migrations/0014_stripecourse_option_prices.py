# Generated by Django 4.2.2 on 2023-07-08 14:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0013_coursepayment_amount_coursepayment_option_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="stripecourse",
            name="option_prices",
            field=models.JSONField(default={}),
            preserve_default=False,
        ),
    ]
