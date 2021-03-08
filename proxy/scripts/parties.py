from typing import Dict, Optional
from proxy.scripts.wikipedia import get_wikipedia_abstract, get_wikipedia_info_box
import requests
from proxy.scripts.serializers.parties import serialize_parliament_info
from threading import Thread

PARTY_NAME_MAP = {
    "s": "Socialdemokraterna",
    "m": "Moderaterna",
    "sd": "Sverigedemokraterna",
    "c": "Centerpartiet",
    "v": "Vänsterpartiet",
    "kd": "Kristdemokraterna",
    "l": "Liberalerna",
    "mp": "Miljöpartiet",
}

PARLIAMENT_INFO_URL = "https://www.riksdagen.se/sv/ledamoter-partier/{}"


def get_parliament_information(party: str, result_object: Optional[Dict] = None):
    url_param = PARTY_NAME_MAP[party].lower().replace("ä", "a").replace("å", "a").replace("ö", "o")

    res = requests.get(PARLIAMENT_INFO_URL.format(url_param))
    data = res.text
    info = serialize_parliament_info(data, party)

    if result_object is not None:
        result_object["info"] = info
    else:
        return info


def get_party(party: str):
    result_object: Dict = {}
    wikipedia_abstract_thread = Thread(target=get_wikipedia_abstract, args=(party, result_object))
    wikipedia_info_box_thread = Thread(target=get_wikipedia_info_box, args=(party, result_object))
    parliament_information_thread = Thread(target=get_parliament_information, args=(party, result_object))

    wikipedia_abstract_thread.start()
    wikipedia_info_box_thread.start()
    parliament_information_thread.start()

    wikipedia_abstract_thread.join()
    wikipedia_info_box_thread.join()
    parliament_information_thread.join()

    return result_object
