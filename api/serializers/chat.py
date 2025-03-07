from rest_framework import serializers

from api.models import Chat


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ["id", "section", "role", "content", "created_at"]
