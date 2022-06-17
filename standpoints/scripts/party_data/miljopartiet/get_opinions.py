from typing import List

import requests
from bs4 import BeautifulSoup

OPINION_TAG = "h2:-soup-contains('Miljöpartiet vill') + ul li"
SECONDARY_TAG = "p:-soup-contains('Miljöpartiet vill') + ul li"
THITD_TAG = "p:-soup-contains('Vi vill också förändra nuvarande system genom att:') + ul li"


def get_opinions(url: str) -> List[str]:
    page = requests.get(url)
    # Override encoding
    page.encoding = "utf-8"
    soup = BeautifulSoup(page.text, "html.parser")

    opinions = soup.select(OPINION_TAG)

    if len(opinions) == 0:
        opinions = soup.select(SECONDARY_TAG)

    if len(opinions) == 0:
        opinions = soup.select(THITD_TAG)

    return list(map(lambda el: el.text.strip(), opinions))
