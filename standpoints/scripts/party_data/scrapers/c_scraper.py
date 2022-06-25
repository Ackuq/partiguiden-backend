from typing import List

from ..party_scraper import PartyScraper


class CScraper(PartyScraper):
    @property
    def base_url(self) -> str:
        return "https://www.centerpartiet.se"

    @property
    def list_path(self) -> str:
        return "/var-politik/politik-a-o"

    @property
    def list_selector(self) -> str:
        return ".sol-collapse-decoration.sol-political-area a"

    @property
    def absolute_urls(self) -> bool:
        return False

    @property
    def path_regex(self) -> str:
        return r"\/[/.a-zA-Z0-9-]+"

    @property
    def opinion_tags(self) -> List[str]:
        return ["p:-soup-contains('vill') + ul > li", "p:-soup-contains('anser') + ul > li"]
