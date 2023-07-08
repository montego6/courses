# Generated by Django 4.2.2 on 2023-07-08 14:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0012_coursepayment"),
    ]

    operations = [
        migrations.AddField(
            model_name="coursepayment",
            name="amount",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="coursepayment",
            name="option",
            field=models.CharField(
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
        migrations.AlterField(
            model_name="additionalfile",
            name="option",
            field=models.CharField(
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
        migrations.AlterField(
            model_name="homework",
            name="option",
            field=models.CharField(
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
        migrations.AlterField(
            model_name="lesson",
            name="option",
            field=models.CharField(
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
        migrations.AlterField(
            model_name="test",
            name="option",
            field=models.CharField(
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
    ]
