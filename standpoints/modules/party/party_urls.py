from django.urls import path

from .party_requests import get_parties, get_party_standpoint

party_urls = [
    path("party", get_parties, name="parties"),
    path("party/<party>/", get_party_standpoint, name="party"),
]
