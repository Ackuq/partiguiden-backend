import re
from threading import Thread
from typing import Dict, List

from proxy.scripts.vote import get_vote_result


def title_trim(title: str):
    return re.split(r"[0-9]{4}\/[0-9]{2}:[A-ö]{0,4}[0-9]{0,4}", title)[1].strip()


def serialize_vote(data: Dict, result_list: List, i: int):
    title = title_trim(data["sokdata"]["titel"])

    proposition: int = int(data["tempbeteckning"])
    denomination: str = data["beteckning"]

    id: str = data["id"]

    document_id = "{}01{}".format(id[0:2], denomination.split("p")[0])

    results = get_vote_result(document_id, proposition)

    result_list[i] = {
        "title": title,
        "results": results["results"],
        "subtitle": results["subtitle"],
        "authority": data["organ"],
        "document_id": document_id,
        "proposition": proposition,
    }


def serialize_votes(data: Dict):
    document_list = data["dokumentlista"]

    pages = int(document_list["@sidor"])

    votes = document_list.get("dokument")

    if votes is None or pages == 0:
        return {"pages": pages, "votes": []}

    threads: List[Thread] = []
    result_list = [None] * len(votes)

    for i, vote in enumerate(votes):
        thread = Thread(target=serialize_vote, args=(vote, result_list, i))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return {"pages": pages, "votes": result_list}
