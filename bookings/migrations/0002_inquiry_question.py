# Generated by Django 4.2 on 2023-10-06 12:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bookings", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="inquiry",
            name="question",
            field=models.CharField(default="some questiong", max_length=500),
            preserve_default=False,
        ),
    ]
