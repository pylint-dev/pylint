import functools


@functools.cache
def cached_fibonacci(n):
    if n in {0, 1}:
        return n
    return cached_fibonacci(n - 1) + cached_fibonacci(n - 2)


class Fibonnaci:
    def __init__(self):
        self.result = []

    def fibonacci(self, n):
        self.result.append(cached_fibonacci(n))
