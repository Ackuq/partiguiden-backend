from typing import List

import requests
from bs4 import BeautifulSoup

OPINION_TAG = "h2:-soup-contains('Miljöpartiet vill') + ul li"


def get_opinions(url: str) -> List[str]:
    page = requests.get(url)

    soup = BeautifulSoup(page.text, "html.parser")

    opinions = soup.select(OPINION_TAG)

    return list(map(lambda el: el.text.strip(), opinions))
