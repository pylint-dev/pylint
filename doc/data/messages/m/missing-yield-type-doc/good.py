from typing import Iterator


def even_number_under(n: int) -> Iterator[int]:
    """Prints even numbers smaller than n.
    Args:
        n: Upper limit of even numbers.

    Yields:
        even numbers
    """
    for i in range(n):
        if i % 2 == 1:
            continue
        yield i
