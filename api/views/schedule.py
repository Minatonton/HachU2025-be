from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, mixins

from api.models import Schedule
from api.serializers.schedule import ScheduleSerializer


class ScheduleViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        year = self.request.query_params.get("year")
        if year:
            queryset = queryset.filter(date__year=year)
        month = self.request.query_params.get("month")
        if month:
            queryset = queryset.filter(date__month=month)
        day = self.request.query_params.get("day")
        if day:
            queryset = queryset.filter(date__day=day)
        return queryset

    def create(self, request, *args, **kwargs):
        request.data.update(user=request.user.pk)
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=["POST"])
    def suggest(self, request, *args, **kwargs):
        text = request.data.get("text", "")
        queryset = Schedule.objects.filter(user=request.user)[:5]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["PATCH"], url_path="bulk-register")
    def bulk_is_register(self, request, *args, **kwargs):
        ids = request.data.get("ids", [])
        if not ids:
            return Response({"error": "IDs are required"}, status=status.HTTP_400_BAD_REQUEST)
        Schedule.objects.filter(id__in=ids).update(is_registered=True)
        return Response(status=status.HTTP_204_NO_CONTENT)
