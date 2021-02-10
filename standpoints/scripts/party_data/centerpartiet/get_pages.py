from typing import List

import requests
from bs4 import BeautifulSoup

from ..data_entry import DataEntry
from .get_opinions import get_opinions

URL = "https://www.centerpartiet.se/var-politik/politik-a-o"

SELECTOR = ".sol-collapse-decoration.sol-political-area a"


def get_pages() -> List[DataEntry]:
    page = requests.get(URL)

    soup = BeautifulSoup(page.text, "html.parser")
    pages = soup.select(SELECTOR)

    result: List[DataEntry] = []

    for page in pages:
        title = page.text
        url = "https://www.centerpartiet.se" + page["href"]
        opinions = get_opinions(url)

        result.append(DataEntry(title, url, opinions))

    return result
