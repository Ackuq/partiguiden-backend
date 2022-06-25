from typing import List

from ..party_scraper import PartyScraper


class SScraper(PartyScraper):
    @property
    def base_url(self) -> str:
        return "https://www.socialdemokraterna.se"

    @property
    def list_path(self) -> str:
        return "/var-politik/a-till-o"

    @property
    def list_selector(self) -> str:
        return ".sap-ao-lettergroup-topic-box > a"

    @property
    def opinion_tags(self) -> List[str]:
        return ["div.sv-text-portlet.sv-use-margins > div.sv-text-portlet-content > ul > li"]

    @property
    def absolute_urls(self) -> bool:
        return False
