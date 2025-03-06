import uuid

from django.db import models

from .diary import Diary


class DiaryImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    diary = models.ForeignKey(
        Diary,
        on_delete=models.CASCADE,
        related_name="diary_images",
        verbose_name="日記",
    )
    image = models.ImageField("写真", upload_to="image/diary_image", blank=True)

    class Meta:
        verbose_name = "日記写真"
        verbose_name_plural = "日記写真"

    def __str__(self) -> str:
        return str(self.id)
