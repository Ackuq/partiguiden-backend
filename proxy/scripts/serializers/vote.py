import re
from functools import reduce
from typing import Dict, List


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


REFERENCE_REGEX = r"[0-9]{4}\/[0-9]{2}:[A-ö]{0,4}[0-9]{0,4}"


def create_references(unparsed_proposition: str, references: List):
    proposition = re.sub(r"(<br>)|<BR\/>", "", unparsed_proposition)

    referenced_documents: List[str] = re.findall(REFERENCE_REGEX, proposition)

    processed_documents = []

    for i, reference in enumerate(referenced_documents):
        start = proposition.index(reference)
        end = proposition.index(referenced_documents[i + 1]) if i < len(referenced_documents) - 1 else len(proposition)

        id = next(r["ref_dok_id"] for r in references if "{}:{}".format(r["ref_dok_rm"], r["ref_dok_bet"]) == reference)

        section = proposition[start:end]

        if ")" in section:
            # Replace EX: "2019/20:3642 av Helena Lindahl m.fl. (C)"
            end_index = section.index(")") + 1
            label = section[0:end_index]
            processed_documents.append((id, label))
            proposition = "[{}]".format(i).join(proposition.split(label))
        else:
            # Just replace the ID, EX: "2019/20:3642"
            processed_documents.append((id, reference))
            proposition = "[{}]".format(i).join(proposition.split(reference))

    return (processed_documents, proposition)


def serialize_vote(data: Dict, proposition_num: int):
    document_status = data["dokumentstatus"]

    unparsed_proposition = document_status["dokutskottsforslag"]["utskottsforslag"]

    authority = document_status["dokument"]["organ"]
    proposition = (
        unparsed_proposition[proposition_num - 1] if isinstance(unparsed_proposition, list) else unparsed_proposition
    )

    processed_documents, proposition_text = create_references(
        proposition["forslag"], document_status["dokreferens"]["referens"]
    )

    document_information = document_status["dokuppgift"]["uppgift"]

    decision = next(info for info in document_information if info["kod"] == "rdbeslut")
    description = next(info for info in document_information if info["kod"] == "notis")
    title = next(info for info in document_information if info["kod"] == "notisrubrik")

    table = proposition["votering_sammanfattning_html"]["table"]
    row = table[len(table) - 1]["tr"] if isinstance(table, list) else table["tr"]

    return {
        "title": title["text"],
        "description": description["text"].strip(),
        "authority": authority,
        "proposition_text": proposition_text,
        "processed_documents": processed_documents,
        "appendix": document_status["dokbilaga"]["bilaga"] if document_status["dokbilaga"] is not None else None,
        "decision": decision["text"] if decision is not None else "",
        "voting": extract_votes(row),
    }
