from django.urls import path

from .standpoint_requests import lookup, standpoint

standpoint_urls = [
    path("standpoint/lookup/", lookup, name="lookup"),
    path("standpoint/", standpoint, name="standpoint"),
]
