from django.urls import path

from .subject_requests import get_subjects, get_subject_standpoints, get_party_subject_standpoints

subject_urls = [
    path("subject/", get_subjects, name="subjects"),
    path("subject/<subject>/", get_subject_standpoints, name="subject"),
    path("subject/<subject>/<party>/", get_party_subject_standpoints, name="party_subject"),
]
