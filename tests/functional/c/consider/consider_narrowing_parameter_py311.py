"""'except*' handlers also guard attribute accesses (Python 3.11+ syntax)."""

# pylint: disable=missing-docstring


def _star_guard(fruit):
    result = ""
    try:
        print(fruit.color)
        result = str(fruit.color)
    except* AttributeError:
        result = "?"
    return result
