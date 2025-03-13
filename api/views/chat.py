from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, mixins

from api.models import Chat, Section
from api.serializers.chat import ChatSerializer
from api.views.settings import image_collection_name, text_collection_name
from src.rag.model import ChatModel
from src.rag.rag import RAG


class ChatViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    rag_model = RAG(
        collection_name_text=text_collection_name, collection_name_image=image_collection_name
    )

    def get_queryset(self):
        return super().get_queryset().filter(section__user=self.request.user)

    def create(self, request, *args, **kwargs):
        request.data.update(user=request.user.pk)
        request.data.update(role=0)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        section_id = request.data.get("section")
        content = request.data.get("content")
        section_instance = get_object_or_404(Section, id=section_id)
        chat_instances = Chat.objects.filter(id=section_id).order_by("-created_at")
        chat_instances_for_rag = [
            ChatModel(role="user" if chat.role == 0 else "assistant", content=chat.content)
            for chat in chat_instances
        ] + [ChatModel(role="user", content=content)]
        response = self.rag_model.get_resonse(chat_instances_for_rag)
        res_chat = Chat.objects.create(section=section_instance, content=response.response, role=1)
        res_serializer = self.get_serializer(res_chat)
        return Response(res_serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=["GET"], detail=True)
    def section(self, request, pk, *args, **kwargs):
        queryset = self.get_queryset().filter(section=pk)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
