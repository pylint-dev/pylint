class Iterator:
    def __init__(self, end, start=0):
        self.n = start
        self.end = end

    def __iter__(self):
        return self

    def __next__(self):
        if self.n <= self.end:
            n = self.n
            self.n += 1
            return n

        raise StopIteration
