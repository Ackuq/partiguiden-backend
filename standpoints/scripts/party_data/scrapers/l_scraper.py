from typing import List

from ..party_scraper import PartyScraper


class LScraper(PartyScraper):
    @property
    def base_url(self) -> str:
        return "https://www.liberalerna.se"

    @property
    def list_path(self) -> str:
        return "/politik-a-o/"

    @property
    def list_selector(self) -> str:
        return ".politicsIdx-list-group a"

    @property
    def opinion_tags(self) -> List[str]:
        return [".spolitik-content.container > .wysiwyg-content p"]
