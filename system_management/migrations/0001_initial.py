# Generated by Django 5.1.3 on 2024-11-23 13:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="SAID",
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
                ("id_number", models.CharField(max_length=13, unique=True)),
                ("date_of_birth", models.DateField()),
                ("gender", models.CharField(max_length=10)),
                ("is_citizen", models.BooleanField()),
                ("search_count", models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name="Holiday",
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
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField()),
                ("date", models.DateField()),
                ("type", models.CharField(max_length=100)),
                (
                    "said",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="system_management.said",
                    ),
                ),
            ],
        ),
    ]
