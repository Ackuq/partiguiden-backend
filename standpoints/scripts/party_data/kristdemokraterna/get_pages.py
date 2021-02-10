from typing import List

import requests
from bs4 import BeautifulSoup

from ..data_entry import DataEntry

URL = "https://kristdemokraterna.se/politik-a-o/"

PARAGRAPH_SELECTOR = ".u-txt-brand"


def get_pages() -> List[DataEntry]:
    page = requests.get(URL)

    soup = BeautifulSoup(page.text, "html.parser")
    paragraphs = soup.select(PARAGRAPH_SELECTOR)

    result: List[DataEntry] = []

    for paragraph in paragraphs:
        title = paragraph.text

        url = URL

        opinions_text: str = paragraph.parent.text.replace(title, "", 1).strip()  # Remove the redundant title start
        opinions = list(filter(len, opinions_text.splitlines()))  # If multiple lines, split and remove empty lines

        if title != "":
            result.append(DataEntry(title, url, opinions))

    return result
