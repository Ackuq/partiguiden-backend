from django.contrib import admin
from django.urls import include, path
from rest_framework.schemas import get_schema_view

schema_view = get_schema_view(title="Example API")

urlpatterns = [
    path("schema", schema_view),
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("", include("standpoints.urls")),
]

