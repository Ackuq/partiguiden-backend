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
        return ".a-o__table.a-o-table.bt tbody tr"

    @property
    def opinion_tags(self) -> List[str]:
        return [":nth-child(2) > *"]

    title_tag = ":nth-child(1)"

    async def _get_standpoint_page(self, element: Tag) -> Union[DataEntry, None]:
        title_tag = element.select_one(self.title_tag)
        if title_tag is None:
            return None
        title = title_tag.text

        title_hash = title.lower().replace(" ", "-").replace("å", "a").replace("ä", "a").replace("ö", "o").strip()

        url = self.base_url + self.list_path + "#" + title_hash

        opinions_tag = element.select(self.opinion_tags[0])

        opinions = [
            opinion.text.strip()
            for opinion in opinions_tag
            if opinion.text != "Länk till relevant dokument" and opinion.name != "ul"
        ]

        if title != "" or url != "":
            return DataEntry(title=title, url=url, opinions=opinions)
        return None
