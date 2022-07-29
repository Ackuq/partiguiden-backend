from typing import List

from ..party_scraper import PartyScraper


class KDScraper(PartyScraper):
    @property
    def base_url(self) -> str:
        return "https://kristdemokraterna.se"

    @property
    def list_path(self) -> str:
        return "/var-politik/politik-a-till-o"

    @property
    def list_selector(self) -> str:
        return ".item .content a"

    @property
    def opinion_tags(self) -> List[str]:
        return [".sv-text-portlet-content .font-normal"]

    @property
    def absolute_urls(self) -> bool:
        return False
