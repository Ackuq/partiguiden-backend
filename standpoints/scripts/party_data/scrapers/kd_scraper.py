import urllib.parse
from typing import List, Union

from bs4 import Tag

from ..data_entry import DataEntry
from ..party_scraper import PartyScraper


class KDScraper(PartyScraper):
    @property
    def base_url(self) -> str:
        return "https://kristdemokraterna.se"

    @property
    def list_path(self) -> str:
        return "/var-politik/politik-a-o/"

    @property
    def list_selector(self) -> str:
        return ".pagecontent .sv-text-portlet .sv-text-portlet-content p strong"

    @property
    def opinion_tags(self) -> List[str]:
        return []

    async def _get_standpoint_page(self, element: Tag) -> Union[DataEntry, None]:
        title = element.text
        # Fallback url, in case we cannot extract ID
        url = self.base_url + self.list_path + "#" + urllib.parse.quote(title.lower())
        # The actual ID is stored in its own element, right above the one containing the actual content
        parent_element = element.parent.parent
        if parent_element is not None:
            id_element = parent_element.previous_sibling
            if id_element is not None and id_element.get("id") is not None:
                url = self.base_url + self.list_path + "#" + id_element["id"]
        print(url)
        opinions_text: str = element.parent.text.replace(title, "", 1).strip()  # Remove the redundant title start
        opinions = list(filter(len, opinions_text.splitlines()))  # If multiple lines, split and remove empty lines

        if title == "":
            return None
        return DataEntry(title, url, opinions)
