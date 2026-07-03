"""
    Pylint score:  -1.67
"""
# pylint: disable=broad-except

def loop():
    """Run a loop."""
    count = 0
    for _ in range(5):
        count += 1
    print(count)
