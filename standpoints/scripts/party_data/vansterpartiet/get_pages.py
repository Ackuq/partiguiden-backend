from typing import List

import requests
from bs4 import BeautifulSoup

from ..data_entry import DataEntry
from .get_opinions import get_opinions

URL = "https://www.vansterpartiet.se/politik-a-o/"

SELECTOR = ".mo-card__cover-link"


def get_pages() -> List[DataEntry]:
    page = requests.get(URL)

    soup = BeautifulSoup(page.text, "html.parser")
    elements = soup.select(SELECTOR)

    result: List[DataEntry] = []

    for element in elements:
        title = element.text
        url = element["href"]
        opinions = get_opinions(url)

        result.append(DataEntry(title, url, opinions))

    return result
