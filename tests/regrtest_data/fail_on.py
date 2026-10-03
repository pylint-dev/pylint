"""
    Pylint score:  -1.67
"""
import nonexistent
# pylint: disable=broad-except


def loop():
    count = 0
    for _ in range(5):
        count += 1
    print(count)
