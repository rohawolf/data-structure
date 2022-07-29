class Stack:
    def __init__(self):
        self._stack = []

    def push(self, data):
        self._stack.append(data)

    def pop(self, default=None):
        if self.is_empty:
            return default

        data = self._stack[-1]
        del self._stack[-1]

        return data

    def peek(self):
        if self.is_empty:
            return None

        data = self._stack[-1]
        return data

    @property
    def is_empty(self):
        return len(self._stack) == 0
