import asyncio
import logging
import re
from abc import abstractmethod
from random import randint
from typing import List, Union

import aiohttp
import requests
from bs4 import BeautifulSoup, Tag

from .data_entry import DataEntry

logger = logging.getLogger(__name__)


def get_or_create_event_loop() -> asyncio.AbstractEventLoop:
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()
        raise ex


class PartyScraper:
    @property
    @abstractmethod
    def base_url(self) -> str:
        return NotImplemented

    @property
    @abstractmethod
    def list_path(self) -> str:
        return NotImplemented

    @property
    @abstractmethod
    def list_selector(self) -> str:
        return NotImplemented

    @property
    def absolute_urls(self) -> bool:
        return True

    @property
    def path_regex(self) -> str:
        return NotImplemented

    @property
    @abstractmethod
    def opinion_tags(self) -> List[str]:
        return NotImplemented

    def _get_opinions(self, soup: BeautifulSoup) -> List[str]:
        for tag in self.opinion_tags:
            opinion_elements = soup.select(tag)
            if len(opinion_elements) > 0:
                break

        return list(map(lambda el: el.text.strip(), opinion_elements))

    async def _get_standpoint_page(self, element: Tag) -> Union[DataEntry, None]:
        title = element.text
        if title == "":
            title = element["title"]
        if not self.absolute_urls:
            if self.path_regex is not NotImplemented:
                match = re.search(self.path_regex, element["href"])
                if not match:
                    logger.warn(f"Failed to extract URL for page {title}, got path {element['href']}")
                    return None
                url = self.base_url + match.group(0)
            else:
                url = self.base_url + element["href"]
        else:
            url = element["href"]
        if url == "":
            logger.warn(f"Failed to extract URL for page {title}, got no path...")
            return None
        # Sleep so we do not get rate limited :)
        await asyncio.sleep(randint(1, 100) / 10)
        async with aiohttp.ClientSession() as session:
            resp = await session.get(url)
            html = await resp.text()
            soup = BeautifulSoup(html, "html.parser")
            opinions = self._get_opinions(soup)
            return DataEntry(title=title, url=url, opinions=opinions)

    def get_pages(self) -> List[DataEntry]:
        loop = get_or_create_event_loop()
        html = requests.get(self.base_url + self.list_path)
        # Override this in case of something failed
        html.encoding = "utf-8"
        soup = BeautifulSoup(html.text, "html.parser")
        elements = soup.select(self.list_selector)
        data_future = asyncio.gather(*[self._get_standpoint_page(element) for element in elements])
        data = loop.run_until_complete(data_future)
        result: List[DataEntry] = list(filter(None, data))
        return result
