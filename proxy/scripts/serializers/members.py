from datetime import date
from typing import Dict, Iterable, Optional

EXCLUDE_INFORMATION = [
    "sv",
    "en",
    "KandiderarINastaVal",
    "Officiell e-postadress",
    "Föräldrar",
    "Tjänstetelefon",
]


def serialize_information(data: Dict):
    return {"code": data.get("kod", None), "content": data.get("uppgift", None), "type": data.get("typ", None)}


def serialize_task(data: Dict):
    return {
        "authority_code": data.get("organ_kod"),
        "role": data.get("roll_kod"),
        "content": data.get("uppgift"),
        "status": data.get("status"),
        "type": data.get("typ"),
        "from": data.get("from"),
        "to": data.get("tom"),
    }


def serializer_member(data: Dict):
    information: Iterable = []
    tasks: Iterable = []

    unparsed_information = data.get("personuppgift")
    if unparsed_information is not None and unparsed_information["uppgift"] is not None:
        information_rows = unparsed_information["uppgift"]
        filtered_information = filter(lambda a: a.get("kod") not in EXCLUDE_INFORMATION, information_rows)
        information = list(map(serialize_information, filtered_information))

    unparsed_tasks = data.get("personuppdrag")
    if unparsed_tasks is not None and unparsed_tasks["uppdrag"] is not None:
        tasks = list(map(serialize_task, unparsed_tasks["uppdrag"]))

    picture_url: Optional[str] = data.get("bild_url_192")

    is_leader = False

    for task in tasks:
        if task.get("role") == "Partiledare" and (task["to"] is None or task["to"] == ""):
            is_leader = True
            break

    age = date.today().year - int(data["fodd_ar"])

    return {
        "id": data.get("intressent_id"),
        "source_id": data.get("sourceid"),
        "first_name": data.get("tilltalsnamn"),
        "last_name": data.get("efternamn"),
        "picture_url": picture_url.replace("http://", "https://") if picture_url is not None else "",
        "age": age,
        "party": data.get("parti"),
        "district": data.get("valkrets"),
        "status": data.get("status"),
        "information": information,
        "tasks": tasks,
        "is_leader": is_leader,
    }


def serializer_members(res: Dict):
    return map(serializer_member, res["personlista"]["person"])
