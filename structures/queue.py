class Queue:
    def __init__(self):
        self._queue = []

    def enqueue(self, data):
        return self._queue.append(data)

    def dequeue(self):
        if self.is_empty:
            return None

        return self._queue.pop()

    def peek(self):
        if self.is_empty:
            return None

        return self._queue[0]

    @property
    def is_empty(self):
        return len(self._queue) == 0
