from django.db import models


class RoleChoices(models.IntegerChoices):
    USER = 0, "User"
    AI = 1, "AI"
