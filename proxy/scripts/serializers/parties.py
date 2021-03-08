from threading import Thread
from typing import Dict, List, Tuple

from bs4 import BeautifulSoup

from proxy.scripts.members import fetch_member


def serialize_parliament_info(html: str, party: str):
    soup = BeautifulSoup(html, "html.parser")

    leaders = soup.find(class_="fellows-list")

    leader_threads: List[Tuple[Thread, Dict]] = []

    if leaders is not None:
        for leader in leaders.find_all(class_="fellow-item"):
            role_element = leader.find(class_="fellow-position")
            role = role_element.text if role_element is not None else None

            name_element = leader.find(class_="fellow-name")
            name_list: List[str] = name_element.text.strip().split(" ") if name_element is not None else []

            first_name = name_list.pop(0)
            last_name = " ".join(name_list)

            parliament_query = {
                "fnamn": first_name,
                "enamn": last_name,
                "parti": party,
                "rdlstatus": "samtliga",
                "utformat": "json",
            }
            result_object: Dict = {"role": role}

            thread = Thread(target=fetch_member, args=(parliament_query, result_object))
            thread.start()
            leader_threads.append((thread, result_object))

    all_leaders = []

    for thread, result in leader_threads:
        thread.join()
        all_leaders.append(result)

    return all_leaders
