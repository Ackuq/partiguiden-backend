from argparse import ArgumentParser, BooleanOptionalAction
from typing import List

from .centerpartiet.get_pages import get_pages as get_pages_c
from .data import DataEntry
from .kristdemokraterna.get_pages import get_pages as get_pages_kd
from .liberalerna.get_pages import get_pages as get_pages_l
from .miljopartiet.get_pages import get_pages as get_pages_mp
from .moderaterna.get_pages import get_pages as get_pages_m
from .socialdemokraterna.get_pages import get_pages as get_pages_s
from .sverigedemokraterna.get_pages import get_pages as get_pages_sd
from .vansterpartiet.get_pages import get_pages as get_pages_v


def get_party_data(abbreviation: str) -> List[DataEntry]:
    abbv_upper = abbreviation.upper()
    if abbv_upper == "S":
        return get_pages_s()
    elif abbv_upper == "M":
        return get_pages_m()
    elif abbv_upper == "C":
        return get_pages_c()
    elif abbv_upper == "KD":
        return get_pages_kd()
    elif abbv_upper == "L":
        return get_pages_l()
    elif abbv_upper == "MP":
        return get_pages_mp()
    elif abbv_upper == "SD":
        return get_pages_sd()
    elif abbv_upper == "V":
        return get_pages_v()
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
