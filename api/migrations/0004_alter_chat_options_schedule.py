# Generated by Django 5.1.6 on 2025-03-07 07:34

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0003_chat_created_at"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="chat",
            options={"verbose_name": "チャット", "verbose_name_plural": "チャット"},
        ),
        migrations.CreateModel(
            name="Schedule",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False
                    ),
                ),
                (
                    "content",
                    models.CharField(blank=True, default="", max_length=10000, verbose_name="内容"),
                ),
                ("date", models.DateField(null=True, verbose_name="日付")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="schedules",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="ユーザー",
                    ),
                ),
            ],
            options={
                "verbose_name": "スケジュール",
                "verbose_name_plural": "スケジュール",
            },
        ),
    ]
