import re
from threading import Thread
from time import sleep
from typing import List

import requests
from bs4 import BeautifulSoup

from ..data import DataEntry, Queue
from .get_opinions import get_opinions

BASE_URL = "https://www.centerpartiet.se"
LIST_PATH = "/var-politik/politik-a-o"

SELECTOR = ".sol-collapse-decoration.sol-political-area a"

PATH_REGEX = r"\/[/.a-zA-Z0-9-]+"


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
        match = re.search(PATH_REGEX, element["href"])
        if match:
            url = BASE_URL + match.group(0)
            thread = Thread(
                target=get_opinions_wrapper,
                args=(queue, title, url),
            )
            # Sleep so we do not get rate limited
            sleep(0.1)
            thread.start()
            threads.append(thread)
        else:
            print(f"Failed to extract URL for page {title}, got path {element['href']}")

    for thread in threads:
        thread.join()

    return queue.get()
