"""https://github.com/PyCQA/pylint/issues/2615"""
def main():
    """When evaluating except blocks, assume try statements fail."""
    try:
        res = 1 / 0
        res = 42
    except ZeroDivisionError:
        print(res)  # [used-before-assignment]
    print(res)
