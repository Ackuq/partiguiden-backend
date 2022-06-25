from typing import List

from bs4 import BeautifulSoup

from ..party_scraper import PartyScraper

OPINION_TAG = "p:-soup-contains('Vänsterpartiet vill bland annat:') + ul li"
SECONDARY_TAG = ".or-wysiwyg.or-wysiwyg--article.or-wysiwyg--theme-red-white strong"


class VScraper(PartyScraper):
    @property
    def base_url(self) -> str:
        return "https://www.vansterpartiet.se"

    @property
    def list_path(self) -> str:
        return "/politik-a-o/"

    @property
    def list_selector(self) -> str:
        return ".mo-card__cover-link"

    @property
    def opinion_tags(self) -> List[str]:
        return [
            "p:-soup-contains('Vänsterpartiet vill bland annat:') + ul li",
            ".or-wysiwyg.or-wysiwyg--article.or-wysiwyg--theme-red-white strong",
        ]

    def _get_opinions(self, soup: BeautifulSoup) -> List[str]:
        opinions = soup.select(self.opinion_tags[0])
        if len(opinions) == 0:
            secondary = soup.select(self.opinion_tags[1])
            if len(secondary) != 0:
                return [secondary.pop(0).text.strip()]
            else:
                return []
        return list(map(lambda el: el.text.strip(), opinions))
