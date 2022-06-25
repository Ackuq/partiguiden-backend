from typing import List, Union

from bs4 import Tag

from ..data_entry import DataEntry
from ..party_scraper import PartyScraper


class SDScraper(PartyScraper):
    @property
    def base_url(self) -> str:
        return "https://sd.se"

    @property
    def list_path(self) -> str:
        return "/a-o/"

    @property
    def list_selector(self) -> str:
        return ".post-row.post-type-our-politics"

    @property
    def opinion_tags(self) -> List[str]:
        return [":nth-child(2)"]

    title_tag = ":nth-child(1) > a"

    async def _get_standpoint_page(self, element: Tag) -> Union[DataEntry, None]:
        title_tag = element.select(self.title_tag).pop()
        title = title_tag.text

        url = title_tag["href"]

        opinions_tag = element.select(self.opinion_tags[0]).pop()
        opinions = opinions_tag.text.split("\n\n")

        if title != "" or url != "":
            return DataEntry(title=title, url=url, opinions=opinions)
        return None
