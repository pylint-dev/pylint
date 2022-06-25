class Iterator:
    def __init__(self, end, start=0):
        self.n = start
        self.end = end

    def __iter__(self):  # [non-iterator-returned]
        return self
