from functools import reduce
from typing import Dict


def extract_votes(row):
    voting = {}
    entries = row[2:]

    for entry in entries:
        td = entry["td"]
        if isinstance(td, list):
            party_votes = {
                "yes": td[1],
                "no": td[2],
                "refrain": td[3],
                "abscent": td[4],
            }
            voting[td[0]] = party_votes

    return voting


DECISION = ["yes", "no", "refrain"]


def get_max_vote(party_votes: Dict):
    result = {"yes": [], "no": [], "winner": "draw"}

    party_votes.pop("-")
    total = party_votes.pop("Totalt")

    yes_total = int(total["yes"])
    no_total = int(total["no"])

    if yes_total != no_total:
        result["winner"] = "yes" if yes_total > no_total else "no"

    for party, votes in party_votes.items():
        vote: str = reduce(lambda a, b: a if int(votes[a]) > int(votes[b]) else b, DECISION, "yes")

        if vote == "yes" or vote == "no":
            result[vote].append(party)  # type: ignore

    return result


def serialize_vote_result(data: Dict, num: int):
    document_status = data["dokumentstatus"]
    proposal = document_status["dokutskottsforslag"]["utskottsforslag"]

    vote = proposal[num - 1] if isinstance(proposal, list) else proposal

    table = vote["votering_sammanfattning_html"]["table"]
    table_row = table[len(table) - 1]["tr"] if isinstance(table, list) else table["tr"]

    return {"results": get_max_vote(extract_votes(table_row)), "subtitle": vote["rubrik"]}
