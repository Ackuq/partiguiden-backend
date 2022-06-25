from typing import List

from ..party_scraper import PartyScraper

OPINION_TAG = ".site-main__article.site-main__entry-content ul li"
OPINION_TAG_SECOND = ".site-main__article.site-main__entry-content h2:-soup-contains('Moderaterna vill')"


class MScraper(PartyScraper):
    @property
    def base_url(self) -> str:
        return "https://moderaterna.se"

    @property
    def list_path(self) -> str:
        return "/var-politik"

    @property
    def list_selector(self) -> str:
        return ".search-subjects__content--search__form--list__subjects ul li a"

    @property
    def opinion_tags(self) -> List[str]:
        return [
            ".site-main__article.site-main__entry-content ul li",
            ".site-main__article.site-main__entry-content h2:-soup-contains('Moderaterna vill')",
        ]
