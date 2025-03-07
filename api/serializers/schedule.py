from rest_framework import serializers

from api.models import Schedule


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ["id", "user", "content", "date"]
