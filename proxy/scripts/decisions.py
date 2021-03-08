from typing import Dict
from proxy.scripts import BASE_URL
from proxy.scripts.serializers.decisions import decisions_serializer
import requests
from django.http.request import QueryDict


def get_decisions(query: QueryDict):
    parliament_query = {
        "doktyp": "bet",
        "dokstat": "beslutade",
        "sortorder": "desc",
        "utformat": "json",
        "sok": query.get("search", ""),
        "sort": "rel" if query.__contains__("search") else "datum",
        "org": query.get("org", ""),
        "p": query.get("page", ""),
    }

    response = requests.get("{}/dokumentlista/".format(BASE_URL), params=parliament_query)
    data: Dict = response.json()

    return decisions_serializer(data)
