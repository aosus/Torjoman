# Generated by Django 4.1.1 on 2022-09-30 08:32

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("translation", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Translator",
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
                    "uuid",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "number_of_words",
                    models.IntegerField(verbose_name="Number of words to send"),
                ),
                ("send_time", models.TimeField()),
                (
                    "translated_words",
                    models.ManyToManyField(blank=True, to="translation.word"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Platform",
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
                ("name", models.CharField(max_length=250)),
                ("base_url", models.URLField()),
                ("is_active", models.BooleanField(default=True)),
                (
                    "translators",
                    models.ManyToManyField(blank=True, to="translators.translator"),
                ),
            ],
        ),
    ]
