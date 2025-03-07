from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, mixins

from api.models import Chat, Section
from api.serializers.chat import ChatSerializer


class ChatViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def get_queryset(self):
        return super().get_queryset().filter(section__user=self.request.user)

    def create(self, request, *args, **kwargs):
        request.data.update(user=request.user.pk)
        request.data.update(role=0)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        section_id = request.data.get("section")
        section_instance = get_object_or_404(Section, id=section_id)
        res_chat = Chat.objects.create(section=section_instance, content="", role=1)
        res_serializer = self.get_serializer(res_chat)
        return Response(res_serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=["GET"], detail=True)
    def section(self, request, pk, *args, **kwargs):
        queryset = self.get_queryset().filter(section=pk)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
