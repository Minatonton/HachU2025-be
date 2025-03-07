from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.models import Diary
from api.serializers.diary import DiaryCreateSerializer, DiarySerializer
from src.rag.insert import insert_base64
from src.rag.model import Base64Info
from src.rag.search_model import SearchModel
from src.rag.setup import setup_base64_collection
from src.rag.utils import get_text_from_base64


class DiaryViewSet(ModelViewSet):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer
    text_collection_name = "text_base64_search_model_sample"
    image_collection_name = "image_base64_search_model_sample"
    text_collection = setup_base64_collection(text_collection_name)
    image_collection = setup_base64_collection(image_collection_name)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return DiaryCreateSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        request.data.update(user=request.user.pk)
        base64_content = request.data["image"]
        info = get_text_from_base64(base64_content)
        insert_base64(
            self.text_collection,
            [Base64Info(base64_content=base64_content, info=info)],
            SearchModel.TEXT,
        )
        insert_base64(
            self.image_collection,
            [Base64Info(base64_content=base64_content, info=info)],
            SearchModel.IMAGE_TEXT,
        )
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        date = self.kwargs.get("pk")
        instance = get_object_or_404(Diary, date=date)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
