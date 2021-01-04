from typing import List
import requests
from bs4 import BeautifulSoup

OPINION_TAG = "div.sv-text-portlet.sv-use-margins > div.sv-text-portlet-content > ul > li"


def get_opinions(url: str) -> List[str]:
    page = requests.get(url)

    soup = BeautifulSoup(page.text, "html.parser")

    opinions = soup.select(OPINION_TAG)

    return list(map(lambda el: el.text, opinions))
