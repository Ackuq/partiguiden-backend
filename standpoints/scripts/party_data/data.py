from typing import List


class DataEntry:
    """
    Contains data fetched from website
    """

    def __init__(self, title: str, url: str, opinions: List[str]) -> None:
        self.title = title
        self.url = url
        self.opinions = opinions

    title: str
    url: str
    opinions: List[str]


class Queue:
    def __init__(self):
        self.queue: List[DataEntry] = []

    def enqueue(self, data: DataEntry):
        self.queue.append(data)
        return data

    def get(self) -> List[DataEntry]:
        return self.queue
