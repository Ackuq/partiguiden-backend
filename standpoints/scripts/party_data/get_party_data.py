import logging
from argparse import ArgumentParser
from typing import List, Optional

from .data_entry import DataEntry
from .scrapers import CScraper, KDScraper, LScraper, MPScraper, MScraper, SDScraper, SScraper, VScraper

logger = logging.getLogger(__name__)


def get_party_data(abbreviation: str, limit: Optional[int] = None) -> List[DataEntry]:
    abbv_upper = abbreviation.upper()
    if abbv_upper == "S":
        return SScraper().get_pages(limit)
    elif abbv_upper == "M":
        return MScraper().get_pages(limit)
    elif abbv_upper == "C":
        return CScraper().get_pages(limit)
    elif abbv_upper == "KD":
        return KDScraper().get_pages(limit)
    elif abbv_upper == "L":
        return LScraper().get_pages(limit)
    elif abbv_upper == "MP":
        return MPScraper().get_pages(limit)
    elif abbv_upper == "SD":
        return SDScraper().get_pages(limit)
    elif abbv_upper == "V":
        return VScraper().get_pages(limit)
    else:
        logger.warn(f"Could not find scraper for party {abbv_upper}")
        return []


def test(party_abbrev: str, preview: bool, limit: Optional[int] = None):
    all_data = get_party_data(party_abbrev, limit)

    logger.info("Number of entries: {}".format(len(all_data)))
    logger.info("Number of entries without content: {}".format(len([d for d in all_data if len(d.opinions) == 0])))
    for data in all_data:
        if len(data.title) > 100:
            logger.warn(f"INVALID TITLE: {data.title}")
        if len(data.url) > 150:
            logger.warn(f"INVALID URL: {data.url}")
        if len(data.opinions) == 0:
            logger.warn(f"No content for {data.title} at {data.url}")
    if preview:
        for d in all_data:
            logger.info(f"\n{d.url}\n{d.title}\n{d.opinions}")


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format="[{levelname} {asctime}] {name} - {message}",
        style="{",
        handlers=[logging.StreamHandler()],
    )
    parser = ArgumentParser("test_party_data", description="Test party data extraction")

    parser.add_argument("--party", "-p", required=True, type=str, help="The party to extract data from")
    parser.add_argument("--preview", "-s", action="store_true", help="Preview the data")
    parser.add_argument("--limit", "-l", required=False, type=int, help="Max number of entries")

    args = parser.parse_args()

    test(args.party, args.preview, args.limit)


if __name__ == "__main__":
    main()
