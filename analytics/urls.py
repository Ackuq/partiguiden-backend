from django.urls import path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

urlpatterns = [path("popular/", views.PopularView.as_view())] + router.urls
