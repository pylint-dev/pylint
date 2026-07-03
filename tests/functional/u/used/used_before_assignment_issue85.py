"""https://github.com/pylint-dev/pylint/issues/85"""
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


def try_except_finally_assignment_in_both_try_and_except():
    """Assignment of the name in both try and except blocks is fine."""
    try:
        res = 1 / 0
    except ZeroDivisionError:
        res = 0
    finally:
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


def try_except_finally_nested_in_finally():
    """Until Pylint comes to a consensus on requiring all except handlers to
    define a name, raise, or return (https://github.com/pylint-dev/pylint/issues/5524),
    Pylint assumes statements in try blocks succeed when accessed *after*
    except or finally blocks and fail when accessed *in* except or finally
    blocks.)
    """
    try:
        outer_times = 1
    finally:
        try:
            inner_times = 1
        except TypeError:
            pass
        finally:
            print(outer_times)  # [used-before-assignment]
        print(inner_times)  # see docstring: might emit in a future version


def try_except_finally_nested_in_finally_2():
    """Neither name is accessed after a finally block."""
    try:
        outer_times = 1
    finally:
        try:
            inner_times = 1
        except TypeError:
            pass
        finally:
            print(inner_times)  # [used-before-assignment]
        print(outer_times)  # [used-before-assignment]


def try_except_finally_nested_in_finally_3():
    """One name is never accessed after a finally block, but just emit
    once per name.
    """
    try:
        outer_times = 1
    finally:
        try:
            inner_times = 1
        except TypeError:
            pass
        finally:
            print(inner_times)  # [used-before-assignment]
            print(outer_times)  # [used-before-assignment]
        print(inner_times)
        # used-before-assignment is only raised once per name
        print(outer_times)


def try_except_finally_nested_in_finally_4():
    """Triple nesting: don't assume direct parentages of outer try/finally
    and inner try/finally.
    """
    try:
        outer_times = 1
    finally:
        try:
            pass
        finally:
            try:
                inner_times = 1
            except TypeError:
                pass
            finally:
                print(inner_times)  # [used-before-assignment]
                print(outer_times)  # [used-before-assignment]
            print(inner_times)
            # used-before-assignment is only raised once per name
            print(outer_times)
