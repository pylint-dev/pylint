"""https://github.com/pylint-dev/pylint/issues/5780"""


def used_in_handler_then_after_try():
    """A use inside the handler should not hide a later use after the try."""
    try:
        pass
    except ValueError:
        msg = "ha"
        print(msg)
    print(msg)  # [used-before-assignment]
    print(msg)


def defined_in_two_handlers():
    """The name is defined and used in the first of two handlers."""
    try:
        pass
    except ValueError:
        msg = "ha"
        print(msg)
    except TypeError:
        msg = "ho"
    print(msg)  # [used-before-assignment]


def used_in_sibling_handler():
    """The name is defined and used in one handler, then used in another."""
    try:
        pass
    except ValueError:
        msg = "ha"
        print(msg)
    except TypeError:
        print(msg)  # [used-before-assignment]


def defined_before_try():
    """An assignment before the try is certain."""
    msg = "default"
    try:
        pass
    except ValueError:
        msg = "ha"
        print(msg)
    print(msg)


def defined_after_handler():
    """An assignment after the handler is certain."""
    try:
        pass
    except ValueError:
        msg = "ha"
        print(msg)
    msg = "default"
    print(msg)


def try_block_returns():
    """The handler must have executed if the try block returns."""
    try:
        return None
    except ValueError:
        msg = "ha"
        print(msg)
    print(msg)
    return None


def used_in_comprehension():
    """The comprehension use is not reported, but it does not hide a later
    plain use."""
    try:
        pass
    except ValueError:
        msg = "ha"
        print(msg)
    print([msg for _ in range(1)])
    print(msg)  # [used-before-assignment]


def used_only_in_handler():
    """A use inside the handler only is fine."""
    try:
        pass
    except ValueError:
        msg = "ha"
        print(msg)


def bound_by_later_except_as():
    """The name is bound by the handler of a later try."""
    try:
        pass
    except ValueError:
        err = None
        print(err)
    try:
        pass
    except TypeError as err:
        print(err)


def bound_by_sibling_except_as():
    """The name is bound by a sibling handler."""
    try:
        pass
    except ValueError:
        msg = 1
        print(msg)
    except TypeError as msg:
        print(msg)


def defined_under_if_in_handler(x):
    """The definition is under an if inside the handler."""
    try:
        pass
    except ValueError:
        if x:
            msg = "a"
            print(msg)
    print(msg)  # [possibly-used-before-assignment]


def try_under_if(x):
    """The try is nested under an if."""
    if x:
        try:
            pass
        except ValueError:
            msg = "a"
            print(msg)
    print(msg)  # [possibly-used-before-assignment]


def try_under_always_false_test():
    """The try is in the else branch of an always false test."""
    if False:  # pylint: disable=using-constant-test
        pass
    else:
        try:
            pass
        except ValueError:
            msg = "a"
            print(msg)
    print(msg)  # [used-before-assignment]
