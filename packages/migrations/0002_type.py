# Generated by Django 4.2 on 2023-09-29 16:18

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("packages", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Type",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=100)),
            ],
        ),
    ]
