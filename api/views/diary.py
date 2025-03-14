from datetime import date

from django.shortcuts import get_list_or_404, get_object_or_404
from django.utils.timezone import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.models import Diary
from api.serializers.diary import DiaryCreateSerializer, DiarySerializer
from api.views.settings import image_collection_name, text_collection_name
from src.rag.insert import insert
from src.rag.model import ImageInfo
from src.rag.search_model import SearchModel
from src.rag.setup import setup
from src.rag.utils import get_text_from_image_url


class DiaryViewSet(ModelViewSet):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer
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
        request.data.update(date=self.validate_date(request.data["date"]))
        serializer = self.get_serializer(data=request.data)
        image_content = request.data["image"]
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        image_url = serializer.data.get("image", "") if image_content != "" else ""
        text_info = request.data["content"]
        image_info = get_text_from_image_url(image_url) if image_url != "" else ""
        id = serializer.data.get("id")
        insert(
            self.text_collection,
            [ImageInfo(id=id, image_url=image_url, info=text_info)],
            SearchModel.TEXT,
        )
        # 画像があり、かつ画像が保存できていたら、画像情報をRAG検索出来るように保存
        if image_url and image_url != "":
            insert(
                self.image_collection,
                [ImageInfo(id=id, image_url=image_url, info=image_info)],
                SearchModel.IMAGE_TEXT,
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        query_key = self.kwargs.get("pk")
        if len(query_key) == 10:
            instance = get_list_or_404(Diary, date=query_key)  # 日にちで検索
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

    def validate_date(self, value):
        # 日付の形式を修正し、タイムゾーンを設定
        try:
            native_date = datetime.strptime(value, "%Y-%m-%d-%H:%M")
            return date(native_date.year, native_date.month, native_date.day)
        except BaseException:
            raise ValueError("Invalid date format") from None
