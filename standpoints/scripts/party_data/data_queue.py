from typing import List

from standpoints.scripts.party_data.data_entry import DataEntry


class Queue:
    def __init__(self):
        self.queue: List[DataEntry] = []

    def enqueue(self, data: DataEntry):
        self.queue.append(data)
        return data

    def get(self) -> List[DataEntry]:
        return self.queue
