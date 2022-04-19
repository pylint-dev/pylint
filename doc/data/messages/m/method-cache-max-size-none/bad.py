import functools


class Fibonnaci:
    @functools.lru_cache(maxsize=None)  # [method-cache-max-size-none]
    def fibonacci(self, n):
        if n in {0, 1}:
            return n
        return self.fibonacci(n - 1) + self.fibonacci(n - 2)
