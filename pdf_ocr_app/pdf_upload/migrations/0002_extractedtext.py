# Generated by Django 5.1.7 on 2025-03-08 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pdf_upload", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ExtractedText",
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
                ("text", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
