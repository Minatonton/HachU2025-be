from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import status
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
        serializer = self.get_serializer(data=request.data)
        image_content = request.data["image"]
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        image_url = serializer.data.get("image", "") if image_content != "" else ""
        text_info = request.data["content"]
        image_info = get_text_from_image(image_url) if image_url != "" else ""
        id = serializer.data.get("id")
        insert(
            self.text_collection,
            [ImageInfo(id=id, image_path=image_url, info=text_info)],
            SearchModel.TEXT,
        )
        # 画像があり、かつ画像が保存できていたら、画像情報をRAG検索出来るように保存
        if image_url and image_url != "":
            insert(
                self.image_collection,
                [ImageInfo(id=id, image_path=image_url, info=image_info)],
                SearchModel.IMAGE_TEXT,
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        query_key = self.kwargs.get("pk")
        if len(query_key) == 10:
            instance = get_list_or_404(Diary, date=query_key)
            serializer = self.get_serializer(instance, many=True)
            return Response(serializer.data)
        instance = get_object_or_404(Diary, id=query_key)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        id = self.kwargs.get("pk")
        instance = get_object_or_404(Diary, id=id)
        self.perform_destroy(instance)
        self.text_collection.data.delete_by_id(id)
        if instance.image:
            self.image_collection.data.delete_by_id(id)
        return Response(status=status.HTTP_204_NO_CONTENT)
