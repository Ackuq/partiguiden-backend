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
        return "/var-politik/politik-a-o/"

    @property
    def list_selector(self) -> str:
        return ".ModuleWrapper-module--component--W7iGr section a"

    @property
    def opinion_tags(self) -> List[str]:
        return []

    @property
    def absolute_urls(self) -> bool:
        return False

    def _get_opinions(self, soup: BeautifulSoup) -> List[str]:
        opinions: List[str] = []
        preamble = soup.find("div", {"class": "ArticleBody-module--preamble--+K5Nt"})
        if preamble is not None:
            for paragraph in preamble.children:
                opinion = paragraph.text.strip()
                if opinion != "":
                    opinions.append(opinion)
        actions = soup.select_one("p:-soup-contains('Vänsterpartiet vill bland annat:') + p")
        if actions is None:
            actions = soup.select_one("p:-soup-contains('Vänsterpartiet vill bland annat:')")
        if actions is not None:
            opinions = opinions + [
                text.strip()
                for text in actions.text.replace("• ", "").replace("Vänsterpartiet vill bland annat:\n", "").split("\n")
            ]
        return opinions
