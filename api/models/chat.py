import uuid

from django.db import models

from .choices import RoleChoices
from .section import Section


class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name="chat",
        verbose_name="セクション",
    )
    role = models.IntegerField("ロール", choices=RoleChoices.choices, default=0)
    content = models.CharField(
        "内容",
        max_length=10000,
        blank=True,
        default="",
    )

    class Meta:
        verbose_name = "セクション"
        verbose_name_plural = "セクション"

    def __str__(self) -> str:
        return str(self.id)
