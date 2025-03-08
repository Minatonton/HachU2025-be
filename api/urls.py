from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views.chat import ChatViewSet
from api.views.diary import DiaryViewSet
from api.views.gen_image import GenImageView
from api.views.schedule import ScheduleViewSet
from api.views.section import SectionViewSet

router = SimpleRouter()

app_name = "api"

router.register("diary", DiaryViewSet, basename="diary")
router.register("chat", ChatViewSet, basename="chat")
router.register("section", SectionViewSet, basename="section")
router.register("schedule", ScheduleViewSet, basename="schedule")


urlpatterns = [
    path("", include(router.urls)),
    path("gen_image/", GenImageView.as_view(), name="gen_image"),
]
