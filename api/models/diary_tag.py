import uuid

from django.db import models

from .diary import Diary
from .tag import Tag


class DiaryTag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name="diary_tags",
        verbose_name="タグ",
    )
    diary = models.ForeignKey(
        Diary,
        on_delete=models.CASCADE,
        related_name="diary_tags",
        verbose_name="日記",
    )

    class Meta:
        verbose_name = "日記タグ"
        verbose_name_plural = "日記タグ"

    def __str__(self) -> str:
        return str(self.id)
