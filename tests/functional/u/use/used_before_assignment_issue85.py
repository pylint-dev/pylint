"""https://github.com/PyCQA/pylint/issues/85"""
def main():
    """When evaluating finally blocks, assume try statements fail."""
    try:
        res = 1 / 0
        res = 42
    finally:
        print(res)  # [used-before-assignment]
    print(res)
