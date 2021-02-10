from typing import List


class DataEntry:
    """ Contains data fetched from website """

    def __init__(self, title: str, url: str, opinions: List[str]) -> None:
        self.title = title
        self.url = url
        self.opinions = opinions

    title: str
    url: str
    opinions: List[str]
