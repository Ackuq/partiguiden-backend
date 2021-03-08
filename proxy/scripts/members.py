from threading import Thread
from proxy.scripts.serializers.absence import serialize_absence
from proxy.scripts.serializers.members import serializer_member, serializer_members
from typing import Dict, List
from django.http.request import QueryDict
from proxy.scripts import BASE_URL
import requests


def fetch_absence(query: Dict, result_object):
    res = requests.get("{}/voteringlista/".format(BASE_URL), params=query)
    data = res.json()
    if result_object is not None:
        result_object["absence"] = serialize_absence(data)
    else:
        return serialize_absence(data)


def fetch_member(query: Dict, result_object):
    res = requests.get("{}/personlista/".format(BASE_URL), params=query)
    data = res.json()
    member = data["personlista"].get("person")
    if member is not None:
        if result_object is not None:
            result_object["member"] = serializer_member(member)
        else:
            return serializer_member(member)
    else:
        last_name_array: List[str] = query["enamn"].split(" ")
        if len(last_name_array) > 1:
            last_name_array.pop(0)
            new_query = query.copy()
            new_query["enamn"] = " ".join(last_name_array)
            if result_object is not None:
                fetch_member(new_query, result_object)
            else:
                return fetch_member(new_query, result_object)


def search_member(query: QueryDict):
    parliament_query = {
        "fnamn": query.get("first_name", ""),
        "enamn": query.get("last_name", ""),
        "parti": query.get("party", ""),
        "rdlstatus": "samtliga",
        "utformat": "json",
    }

    return fetch_member(parliament_query, None)


def get_member(id: str):
    absence_query = {
        "iid": id,
        "utformat": "json",
        "gruppering": "namn",
    }

    member_query = {
        "iid": id,
        "rdlstatus": "samtliga",
        "utformat": "json",
    }

    result_object: Dict = {}

    absence_thread = Thread(target=fetch_absence, args=(absence_query, result_object))
    member_thread = Thread(target=fetch_member, args=(member_query, result_object))

    absence_thread.start()
    member_thread.start()

    absence_thread.join()
    member_thread.join()

    return result_object


def get_members(query: QueryDict):
    parliament_query = {
        "parti": query.get("party", ""),
        "utformat": "json",
        "sort": "sorteringsnamn",
    }

    res = requests.get("{}/personlista/".format(BASE_URL), params=parliament_query)
    data = res.json()

    return serializer_members(data)
