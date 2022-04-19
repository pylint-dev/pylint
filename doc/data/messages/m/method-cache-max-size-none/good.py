import functools


@functools.cache
def cached_fibonacci(n):
    if n in {0, 1}:
        return n
    return cached_fibonacci(n - 1) + cached_fibonacci(n - 2)


class Fibonnaci:
    def fibonacci(self, n):
        return cached_fibonacci(n)
