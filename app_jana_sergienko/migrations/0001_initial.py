# Generated by Django 4.1.5 on 2023-01-25 07:37

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Contact",
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
                ("name", models.TextField(blank=True, null=True)),
                ("age", models.IntegerField(blank=True, null=True)),
                ("phone", models.TextField(blank=True, null=True)),
            ],
        ),
    ]
