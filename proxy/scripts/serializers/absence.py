from typing import Dict


def serialize_absence(data: Dict):
    votes: Dict = data["voteringlista"].get("votering")
    if votes is not None:
        abscent = int(votes.get("Frånvarande", 0))
        total = int(votes.get("Ja", 0)) + int(votes.get("Nej", 0)) + abscent + int(votes.get("Avstår", 0))
        return round((1 - (abscent / total)) * 100, 1)
    return None
