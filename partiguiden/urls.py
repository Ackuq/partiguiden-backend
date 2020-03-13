from django.contrib import admin
from django.urls import include, path
from rest_framework.schemas import get_schema_view
from rest_framework.authtoken import views

schema_view = get_schema_view(title="Example API")

urlpatterns = [
    path("schema", schema_view),
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api-token-auth/", views.obtain_auth_token, name="api-token-auth"),
    path("", include("standpoints.urls")),
]

