from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("dj_rest_auth.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    from drf_spectacular.views import (
        SpectacularAPIView,
        SpectacularRedocView,
        SpectacularSwaggerView,
    )

    urlpatterns += [
        path("docs/schema/", SpectacularAPIView.as_view(), name="schema"),
        path("docs/schema/redoc/", SpectacularRedocView.as_view(), name="redoc"),
        path("docs/schema/swagger/", SpectacularSwaggerView.as_view(), name="swagger"),
    ]
