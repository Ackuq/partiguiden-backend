from time import sleep
from urllib.parse import quote

import requests

from proxy.scripts.serializers.wikipedia import serialize_abstact, serialize_info_box

WIKIPEDIA_MAP = {
    "s": "Socialdemokraterna_(Sverige)",
    "m": "Moderaterna",
    "sd": "Sverigedemokraterna",
    "c": "Centerpartiet",
    "v": "Vänsterpartiet",
    "kd": "Kristdemokraterna_(Sverige)",
    "l": "Liberalerna",
    "mp": "Miljöpartiet",
}

ABSTRACT_URL = "https://sv.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&redirects=1&titles={}"


def get_wikipedia_abstract(party: str, return_object=None):
    res = requests.get(ABSTRACT_URL.format(quote(WIKIPEDIA_MAP[party].encode("utf-8"))))

    if res.status_code == 429:
        sleep(1)
        return get_wikipedia_abstract(party, return_object)

    data = res.json()
    abstract = serialize_abstact(data)

    if return_object is not None:
        return_object["abstract"] = abstract
    else:
        return abstract


INFO_BOX_URL = "https://sv.wikipedia.org/w/api.php?action=parse&format=json&section=0&prop=text&page={}"


def get_wikipedia_info_box(party: str, return_object=None):
    res = requests.get(INFO_BOX_URL.format(quote(WIKIPEDIA_MAP[party].encode("utf-8"))))

    if res.status_code == 429:
        sleep(1)
        return get_wikipedia_abstract(party, return_object)

    data = res.json()
    info_box = serialize_info_box(data)

    if return_object is not None:
        return_object["info_box"] = info_box
    else:
        return info_box
