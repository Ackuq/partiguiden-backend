from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView
from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("token/", TokenObtainPairView.as_view(), name="token"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("", include("standpoints.urls")),
    path("analytics/", include("analytics.urls")),
    path("proxy/", include("proxy.urls")),
    path(
        "swagger-ui/",
        TemplateView.as_view(template_name="swagger-ui.html", extra_context={"schema_url": "openapi-schema"}),
        name="swagger-ui",
    ),
    path("openapi/", get_schema_view(title="Partiguiden API", version="1.0.0"), name="openapi-schema"),
]
