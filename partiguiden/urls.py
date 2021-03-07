from django.contrib import admin
from django.urls import include, path
from rest_framework.documentation import include_docs_urls
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("token/", TokenObtainPairView.as_view(), name="token"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("", include("standpoints.urls")),
    path("analytics/", include("analytics.urls")),
    path("docs/", include_docs_urls(title="Partiguiden API docs")),
]
