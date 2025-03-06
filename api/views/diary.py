from rest_framework.viewsets import ModelViewSet

from api.models import Diary
from api.serializers.diary import DiaryCreateSerializer, DiarySerializer


class DiaryViewSet(ModelViewSet):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return DiaryCreateSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        request.data.update(user=request.user.pk)
        return super().create(request, *args, **kwargs)
