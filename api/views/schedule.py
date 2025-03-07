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
