from typing import List

import requests
from bs4 import BeautifulSoup

OPINION_TAG = ".site-main__article.site-main__entry-content ul li"
OPINION_TAG_SECOND = ".site-main__article.site-main__entry-content h2:-soup-contains('Moderaterna vill')"


def get_opinions(url: str) -> List[str]:
    page = requests.get(url)

    soup = BeautifulSoup(page.text, "html.parser")

    opinions = soup.select(OPINION_TAG)
    if len(opinions) == 0:
        opinions = soup.select(OPINION_TAG_SECOND)

    return list(map(lambda el: el.text, opinions))
