from rest_framework.viewsets import GenericViewSet, mixins

from api.models import Section
from api.serializers.section import SectionSerializer


class SectionViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        request.data.update(user=request.user.pk)
        return super().create(request, *args, **kwargs)
