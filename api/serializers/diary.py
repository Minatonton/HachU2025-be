from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from api.models import Diary


class DiaryCreateSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Diary
        fields = ["id", "user", "content", "date", "image"]


class DiarySerializer(serializers.ModelSerializer):
    date = serializers.DateField(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Diary
        fields = ["id", "content", "date", "image"]
