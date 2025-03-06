from rest_framework import serializers

from api.models import Diary


class DiaryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = ["id", "user", "content", "date", "image"]


class DiarySerializer(serializers.ModelSerializer):
    date = serializers.DateField(read_only=True)

    class Meta:
        model = Diary
        fields = ["id", "content", "date", "image"]
