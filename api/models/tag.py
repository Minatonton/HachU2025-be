import uuid

from django.db import models


class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        "名前",
        max_length=100,
        blank=True,
        default="",
    )

    class Meta:
        verbose_name = "タグ"
        verbose_name_plural = "タグ"

    def __str__(self) -> str:
        return str(self.name)
