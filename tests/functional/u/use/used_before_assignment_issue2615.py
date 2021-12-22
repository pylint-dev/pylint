"""https://github.com/PyCQA/pylint/issues/2615"""
def main():
    """When evaluating except blocks, assume try statements fail."""
    try:
        res = 1 / 0
        res = 42
        if main():
            res = None
        with open(__file__, encoding="utf-8") as opened_file:
            res = opened_file.readlines()
    except ZeroDivisionError:
        print(res)  # [used-before-assignment]
    print(res)


def nested_except_blocks():
    """Don't confuse except blocks with each other."""
    try:
        res = 1 / 0
        res = 42
        if main():
            res = None
        with open(__file__, encoding="utf-8") as opened_file:
            res = opened_file.readlines()
    except ZeroDivisionError:
        try:
            more_bad_division = 1 / 0
        except ZeroDivisionError:
            print(more_bad_division)  # [used-before-assignment]
            print(res)  # [used-before-assignment]
    print(res)


def name_earlier_in_except_block():
    """Permit the name that might not have been assigned during the try block
    to be defined inside a conditional inside the except block.
    """
    try:
        res = 1 / 0
    except ZeroDivisionError:
        if main():
            res = 10
        else:
            res = 11
        print(res)
