from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.models import Diary
from api.serializers.diary import DiaryCreateSerializer, DiarySerializer
from src.rag.insert import insert
from src.rag.model import ImageInfo
from src.rag.search_model import SearchModel
from src.rag.setup import setup
from src.rag.utils import get_text_from_image


class DiaryViewSet(ModelViewSet):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer
    text_collection_name = "text_search_model_sample"
    image_collection_name = "image_search_model_sample"
    text_collection = setup(text_collection_name)
    image_collection = setup(image_collection_name)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return DiaryCreateSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        request.data.update(user=request.user.pk)
        created_data = super().create(request, *args, **kwargs)
        image_content = request.data["image"]
        image_url = created_data.data["image"] if image_content else ""
        info = get_text_from_image(image_url)
        insert(
            self.text_collection,
            [ImageInfo(image_path=image_url, info=info)],
            SearchModel.TEXT,
        )
        # 画像があれば、画像情報をRAG検索出来るように保存
        if image_content:
            insert(
                self.image_collection,
                [ImageInfo(image_path=image_url, info=info)],
                SearchModel.IMAGE_TEXT,
            )
        return created_data

    def retrieve(self, request, *args, **kwargs):
        date = self.kwargs.get("pk")
        instance = get_object_or_404(Diary, date=date)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
