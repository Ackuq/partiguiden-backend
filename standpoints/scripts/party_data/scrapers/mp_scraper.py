from typing import List

from ..party_scraper import PartyScraper


class MPScraper(PartyScraper):
    @property
    def base_url(self) -> str:
        return "https://www.mp.se"

    @property
    def list_path(self) -> str:
        return "/politik"

    @property
    def list_selector(self) -> str:
        return ".questions > div div.question .question-content a"

    @property
    def opinion_tags(self) -> List[str]:
        return [
            "h2:-soup-contains('Miljöpartiet vill') + ul li",
            "p:-soup-contains('Miljöpartiet vill') + ul li",
            "p:-soup-contains('Vi vill också förändra nuvarande system genom att:') + ul li",
        ]
