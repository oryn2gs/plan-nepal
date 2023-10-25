# Generated by Django 4.2 on 2023-10-18 13:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0003_profile_gender"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="gender",
            field=models.CharField(
                choices=[
                    ("male", "Male"),
                    ("female", "Female"),
                    ("transgender", "Transgender"),
                ],
                max_length=15,
            ),
        ),
    ]
