from argparse import ArgumentParser, BooleanOptionalAction
from typing import List

from .data_entry import DataEntry
from .scrapers import CScraper, KDScraper, LScraper, MPScraper, MScraper, SDScraper, SScraper, VScraper


def get_party_data(abbreviation: str) -> List[DataEntry]:
    abbv_upper = abbreviation.upper()
    if abbv_upper == "S":
        return SScraper().get_pages()
    elif abbv_upper == "M":
        return MScraper().get_pages()
    elif abbv_upper == "C":
        return CScraper().get_pages()
    elif abbv_upper == "KD":
        return KDScraper().get_pages()
    elif abbv_upper == "L":
        return LScraper().get_pages()
    elif abbv_upper == "MP":
        return MPScraper().get_pages()
    elif abbv_upper == "SD":
        return SDScraper().get_pages()
    elif abbv_upper == "V":
        return VScraper().get_pages()
    else:
        return []


def test(party_abbrev: str, preview: bool):
    all_data = get_party_data(party_abbrev)
    print("Number of entries: {}".format(len(all_data)))
    print("Number of entries without content: {}".format(len([d for d in all_data if len(d.opinions) == 0])))
    for data in all_data:
        if len(data.title) > 100:
            print("INVALID TITLE")
            print(data.title)
        if len(data.url) > 150:
            print("INVALID URL")
            print(data.url)
        if len(data.opinions) == 0:
            print("No content for {} at {}".format(data.title, data.url))
    if preview:
        for d in all_data:
            print(d.title)
            print(d.opinions)
            print("--------------")


if __name__ == "__main__":
    parser = ArgumentParser("test_party_data", description="Test party data extraction")

    parser.add_argument("--party", "-p", required=True, type=str, help="The party to extract data from")
    parser.add_argument("--preview", "-s", action=BooleanOptionalAction, type=bool, help="Preview the data")

    args = parser.parse_args()

    test(args.party, args.preview)
