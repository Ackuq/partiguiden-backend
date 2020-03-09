from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("standpoints/", include("standpoints.urls")),
    path("admin/", admin.site.urls),
]
