from threading import Thread
from typing import List

import requests
from bs4 import BeautifulSoup

from ..data import DataEntry, Queue
from .get_opinions import get_opinions

BASE_URL = "https://www.socialdemokraterna.se"

LIST_PATH = "/var-politik/a-till-o"

SELECTOR = ".sap-ao-lettergroup-topic-box > a"


def get_opinions_wrapper(queue: Queue, title: str, url: str):
    opinions = get_opinions(url)
    queue.enqueue(DataEntry(title, url, opinions))


def get_pages() -> List[DataEntry]:
    page = requests.get(BASE_URL + LIST_PATH)

    soup = BeautifulSoup(page.text, "html.parser")
    elements = soup.select(SELECTOR)

    threads: List[Thread] = []
    queue = Queue()

    for element in elements:
        title = element.text

        url = BASE_URL + element["href"]
        thread = Thread(
            target=get_opinions_wrapper,
            args=(queue, title, url),
        )
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return queue.get()
