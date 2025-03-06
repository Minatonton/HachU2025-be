# Generated by Django 5.1.6 on 2025-03-06 06:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="diary",
            name="image",
            field=models.ImageField(blank=True, upload_to="image/diary", verbose_name="写真"),
        ),
        migrations.DeleteModel(
            name="DiaryImage",
        ),
    ]
