"""https://github.com/PyCQA/pylint/issues/85"""
def main():
    """When evaluating finally blocks, assume try statements fail."""
    try:
        res = 1 / 0
        res = 42
    finally:
        print(res)  # [used-before-assignment]
    print(res)


def try_except_finally():
    """When evaluating finally blocks, assume try statements fail."""
    try:
        res = 1 / 0
        res = 42
    except ZeroDivisionError:
        print()
    finally:
        print(res)  # [used-before-assignment]
    print(res)


def try_except_finally_assignment_in_final_block():
    """Assignment of the name in the final block does not warn."""
    try:
        res = 1 / 0
        res = 42
    except ZeroDivisionError:
        print()
    finally:
        res = 999
        print(res)
    print(res)


def try_except_finally_nested_try_finally_in_try():
    """Don't confuse assignments in different finally statements where
    one is nested inside a try.
    """
    try:
        try:
            res = 1 / 0
        finally:
            print(res)  # [used-before-assignment]
        print(1 / 0)
    except ZeroDivisionError:
        print()
    finally:
        res = 999  # this assignment could be confused for that above
        print(res)
    print(res)


def try_except_finally_nested_try_finally_in_finally():
    """Don't confuse assignments in different finally statements where
    one is nested inside a finally.
    """
    try:
        pass
    finally:
        try:
            times = 1
        except TypeError:
            pass
        # Don't emit: only assume the outer try failed
        print(times)
