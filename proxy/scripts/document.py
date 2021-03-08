from django.http.request import QueryDict
from proxy.scripts import BASE_URL
from typing import Dict
import requests


def get_html_document(id: str):
    res = requests.get("{}/dokument/{}".format(BASE_URL, id))
    return res.text


def get_json_document(id: str):
    res = requests.get("{}/dokument/{}.json".format(BASE_URL, id))
    return res.json()


def serialize_member_document(data: Dict):
    return {
        "authority": data.get("organ"),
        "title": data.get("dokumentnamn"),
        "subtitle": data.get("undertitel"),
        "alt_title": data.get("notisrubrik"),
        "id": data.get("id"),
    }


def serialize_member_documents(res: Dict):
    document_list = res["dokumentlista"]
    pages = int(document_list["@sidor"])
    count = int(document_list["@traffar"])

    documents = document_list.get("dokument")

    if documents is None or pages == 0:
        return {"pages": pages, "count": count, "documents": []}

    return {"pages": pages, "count": count, "documents": map(serialize_member_document, documents)}


def get_member_documents(id: str, query: QueryDict):
    parliament_query = {
        "iid": id,
        "p": query.get("page", "1"),
        "avd": "dokument",
        "sort": "datum",
        "sortorder": "datum",
        "utformat": "json",
    }

    res = requests.get("{}/dokumentlista/".format(BASE_URL), params=parliament_query)
    data = res.json()

    return serialize_member_documents(data)
