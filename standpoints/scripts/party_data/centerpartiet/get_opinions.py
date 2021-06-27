from typing import List

import requests
from bs4 import BeautifulSoup

OPINION_TAG = "p:-soup-contains('vill') + ul > li"
SECONDARY_TAG = "p:-soup-contains('anser') + ul > li"


def get_opinions(url: str) -> List[str]:
    page = requests.get(url)

    soup = BeautifulSoup(page.text, "html.parser")

    opinions = soup.select(OPINION_TAG)

    if len(opinions) == 0:
        opinions = soup.select(SECONDARY_TAG)

    return list(map(lambda el: el.text.strip(), opinions))
