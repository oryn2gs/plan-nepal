# Generated by Django 4.2 on 2023-09-29 15:51

from django.db import migrations, models
import testimonials.models


class Migration(migrations.Migration):
    dependencies = [
        (
            "testimonials",
            "0002_alter_testimonial_city_alter_testimonial_content_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="testimonial",
            name="user_image",
            field=models.ImageField(
                default="testimonial/default.png",
                upload_to=testimonials.models.ts_image_fs,
            ),
        ),
    ]
