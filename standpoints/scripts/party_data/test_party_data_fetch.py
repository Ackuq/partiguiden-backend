from .get_party_data import get_party_data


def test(party_abbrev: str):
    all_data = get_party_data(party_abbrev)
    print("Number of entries: {}".format(len(all_data)))
    for data in all_data:
        if len(data.title) > 100:
            print("INVALID TITLE")
            print(data.title)
        if len(data.url) > 150:
            print("INVALID URL")
            print(data.url)
