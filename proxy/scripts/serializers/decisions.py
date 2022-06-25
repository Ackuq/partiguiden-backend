from threading import Thread
from typing import Dict, List, Union

import requests


def check_if_votes_exists(url: str):
    res = requests.get(url)
    data: Dict = res.json()
    document_status: Dict = data["dokumentstatus"]
    document_suggestions: Union[Dict, None] = document_status.get("dokutskottsforslag")
    if document_suggestions is not None:
        suggestions: Union[List, Dict, None] = document_suggestions.get("utskottsforslag")

        if not isinstance(suggestions, list) and suggestions is not None and suggestions["votering_id"] is not None:
            return True
        elif isinstance(suggestions, list) and suggestions is not None:
            for suggestion in suggestions:
                if suggestion["votering_id"] is not None:
                    return True

    return False


def decision_serializer(data: Dict, decisions: List, index: int):
    vote_search_term = "{}:{}".format(data.get("rm"), data.get("beteckning"))

    json_url = "https:{}".format(data.get("dokument_url_text")).replace(".text", ".json")
    votes_exists = check_if_votes_exists(json_url)

    decisions[index] = {
        "id": data.get("id"),
        "paragraph": data.get("notis"),
        "paragraphTitle": data.get("notisrubrik"),
        "authority": data.get("organ"),
        "denomination": data.get("beteckning"),
        "title": data.get("titel"),
        "vote_search_term": vote_search_term,
        "votes_exists": votes_exists,
    }


def decisions_serializer(data: Dict):
    document_list = data["dokumentlista"]
    document: List = document_list["dokument"]
    pages = int(document_list["@sidor"])

    if not document or pages == 0:
        return {"decisions": [], pages: pages}

    decisions = [None] * len(document)
    threads = []

    for i, decision in enumerate(document):
        thread = Thread(target=decision_serializer, args=(decision, decisions, i))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return {"decisions": decisions, "pages": pages}
