import uuid

from django.conf import settings
from django.db import models


class Section(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="sections",
        verbose_name="ユーザー",
    )
    title = models.CharField(
        "タイトル",
        max_length=10000,
        blank=True,
        default="",
    )

    class Meta:
        verbose_name = "セクション"
        verbose_name_plural = "セクション"

    def __str__(self) -> str:
        return str(self.title)
