import functools


class Fibonnaci:
    def __init__(self):
        self.result = []

    @functools.lru_cache(maxsize=None)  # [method-cache-max-size-none]
    def fibonacci(self, n):
        if n in {0, 1}:
            self.result.append(n)
        self.result.append(self.fibonacci(n - 1) + self.fibonacci(n - 2))
