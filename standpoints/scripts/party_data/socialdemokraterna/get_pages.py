from threading import Thread
from typing import List

import requests
from bs4 import BeautifulSoup

from standpoints.scripts.party_data.data_queue import Queue

from ..data_entry import DataEntry
from .get_opinions import get_opinions

URL = "https://www.socialdemokraterna.se/var-politik/a-till-o"

SELECTOR = "li.active.currentpage > ul > li a"


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
        url = "https://www.socialdemokraterna.se" + element["href"]
        thread = Thread(
            target=get_opinions_wrapper,
            args=(queue, title, url),
        )
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return queue.get()
