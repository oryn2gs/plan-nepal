# Generated by Django 4.2 on 2023-09-29 06:51

from django.db import migrations, models
import testimonials.models
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Testimonial",
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
                ("username", models.TextField(max_length=100)),
                ("content", models.CharField(max_length=500)),
                (
                    "user_image",
                    models.ImageField(
                        default="tesimonial/default.png",
                        upload_to=testimonials.models.ts_image_fs,
                    ),
                ),
                ("city", models.TextField(max_length=100)),
                ("country", models.TextField(max_length=100)),
            ],
        ),
    ]
