from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("standpoints.urls")),
    path("admin/", admin.site.urls),
]
