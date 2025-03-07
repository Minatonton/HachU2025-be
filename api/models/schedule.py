import uuid

from django.conf import settings
from django.db import models


class Schedule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="schedules",
        verbose_name="ユーザー",
    )
    content = models.CharField(
        "内容",
        max_length=10000,
        blank=True,
        default="",
    )
    date = models.DateField("日付", null=True)

    class Meta:
        verbose_name = "スケジュール"
        verbose_name_plural = "スケジュール"

    def __str__(self) -> str:
        return str(self.id)
