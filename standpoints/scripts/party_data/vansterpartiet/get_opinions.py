from typing import List

import requests
from bs4 import BeautifulSoup

OPINION_TAG = "p:-soup-contains('Vänsterpartiet vill bland annat:') + ul li"
SECONDARY_TAG = ".or-wysiwyg.or-wysiwyg--article.or-wysiwyg--theme-red-white strong"


def get_opinions(url: str) -> List[str]:
    page = requests.get(url)

    soup = BeautifulSoup(page.text, "html.parser")

    opinions = soup.select(OPINION_TAG)

    if len(opinions) == 0:
        secondary = soup.select(SECONDARY_TAG).pop(0)
        return [secondary.text.strip()]

    return list(map(lambda el: el.text.strip(), opinions))
