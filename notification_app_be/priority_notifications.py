import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from notification_app_be.models import Notification, PriorityNotification
from notification_app_be.logging_helper import log as Log

TYPE_WEIGHTS = {
    "Placement": 20_000_000_000_000,
    "Result":    10_000_000_000_000,
    "Event":     0,
}


def compute_score(notification: Notification) -> float:
    base = TYPE_WEIGHTS.get(notification.Type, 0)
    try:
        ts = datetime.strptime(notification.Timestamp, "%Y-%m-%d %H:%M:%S")
        recency = ts.timestamp() * 1000
    except Exception:
        recency = 0
    return base + recency


class MinHeap:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.heap: list[PriorityNotification] = []

    @property
    def size(self) -> int:
        return len(self.heap)

    def push(self, item: PriorityNotification):
        if len(self.heap) < self.capacity:
            self.heap.append(item)
            self._bubble_up(len(self.heap) - 1)
        elif item.score > self.heap[0].score:
            self.heap[0] = item
            self._sink_down(0)

    def extract_all_sorted(self) -> list[PriorityNotification]:
        return sorted(self.heap, key=lambda x: x.score, reverse=True)

    def _bubble_up(self, index: int):
        while index > 0:
            parent = (index - 1) // 2
            if self.heap[parent].score <= self.heap[index].score:
                break
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            index = parent

    def _sink_down(self, index: int):
        length = len(self.heap)
        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            smallest = index

            if left < length and self.heap[left].score < self.heap[smallest].score:
                smallest = left
            if right < length and self.heap[right].score < self.heap[smallest].score:
                smallest = right
            if smallest == index:
                break

            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            index = smallest


async def get_top10_priority_notifications(notifications: list[Notification]) -> list[PriorityNotification]:
    await Log("backend", "info", "service", "Computing top 10 priority notifications using MinHeap")

    heap = MinHeap(10)
    for notif in notifications:
        if not notif.ID or not notif.Type or not notif.Timestamp:
            continue
        score = compute_score(notif)
        priority_notif = PriorityNotification(**notif.model_dump(), score=score)
        heap.push(priority_notif)

    await Log("backend", "info", "service", "Successfully extracted top 10 priority notifications")
    return heap.extract_all_sorted()
