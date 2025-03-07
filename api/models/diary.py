import uuid

from django.conf import settings
from django.db import models


class Diary(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="diaries",
        verbose_name="ユーザー",
    )
    title = models.CharField(
        "タイトル",
        max_length=200,
        blank=True,
        default="",
    )
    content = models.CharField(
        "内容",
        max_length=10000,
        blank=True,
        default="",
    )
    date = models.DateField("日付", auto_now_add=True)
    image = models.ImageField("写真", upload_to="image/diary", blank=True)

    class Meta:
        verbose_name = "日記"
        verbose_name_plural = "日記"
        constraints = [
            models.UniqueConstraint(
                fields=["date", "user"],
                name="one_user_per_date",
            )
        ]

    def __str__(self) -> str:
        return str(self.id)
