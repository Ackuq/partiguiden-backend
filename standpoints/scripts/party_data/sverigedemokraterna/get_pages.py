from typing import List

import requests
from bs4 import BeautifulSoup

from ..data import DataEntry

URL = "https://sd.se/a-o/"

ROW_SELECTOR = ".post-row.post-type-our-politics"


def get_pages() -> List[DataEntry]:
    page = requests.get(URL)

    soup = BeautifulSoup(page.text, "html.parser")
    rows = soup.select(ROW_SELECTOR)

    result: List[DataEntry] = []

    for row in rows:
        title_tag = row.select(":nth-child(1) > a").pop()
        title = title_tag.text

        url = title_tag["href"]

        opinions_tag = row.select(":nth-child(2)").pop()
        opinions = opinions_tag.text.split("\n\n")

        if title != "" or url != "":
            result.append(DataEntry(title, url, opinions))

    return result
