from .socialdemokraterna.get_pages import get_pages as get_pages_s


def get_party_data(abbreviation: str):
    if abbreviation == "S":
        return get_pages_s()
    else:
        return []
