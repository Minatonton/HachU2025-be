from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views.diary import DiaryViewSet

router = SimpleRouter()

app_name = "api"

router.register("diary", DiaryViewSet, basename="diary")


urlpatterns = [
    path("", include(router.urls)),
]
