# Generated by Django 4.1.1 on 2022-09-21 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("translation", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PullRequest",
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
                ("prid", models.IntegerField()),
                ("words", models.ManyToManyField(blank=True, to="translation.word")),
            ],
        ),
    ]