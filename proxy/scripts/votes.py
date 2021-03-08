from proxy.scripts.serializers.votes import serialize_votes
from proxy.scripts import BASE_URL
import requests
from django.http.request import QueryDict


def get_votes(query: QueryDict):
    parliament_query = {
        "doktyp": "votering",
        "sortorder": "desc",
        "utformat": "json",
        "sok": query.get("search", ""),
        "sort": "rel" if query.__contains__("search") else "datum",
        "org": query.get("org", ""),
        "p": query.get("page", ""),
    }

    res = requests.get("{}/dokumentlista/".format(BASE_URL), params=parliament_query)
    data = res.json()
    return serialize_votes(data)
