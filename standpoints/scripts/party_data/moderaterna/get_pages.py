from threading import Thread
from typing import List

import requests
from bs4 import BeautifulSoup

from ..data import DataEntry, Queue
from .get_opinions import get_opinions

URL = "https://moderaterna.se/var-politik"

SELECTOR = "li.o-our-politics__topics__topic a"


def get_opinions_wrapper(queue: Queue, title: str, url: str):
    opinions = get_opinions(url)
    queue.enqueue(DataEntry(title, url, opinions))


def get_pages() -> List[DataEntry]:
    page = requests.get(URL)

    soup = BeautifulSoup(page.text, "html.parser")
    elements = soup.select(SELECTOR)

    threads: List[Thread] = []
    queue = Queue()

    for element in elements:
        title = element.text
        url = "https://www.moderaterna.se" + element["href"]
        thread = Thread(
            target=get_opinions_wrapper,
            args=(queue, title, url),
        )
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return queue.get()
