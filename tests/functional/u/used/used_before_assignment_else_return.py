"""If the else block returns, it is generally safe to rely on assignments in the except."""


def valid():
    """https://github.com/PyCQA/pylint/issues/6790"""
    try:
        pass
    except ValueError:
        error = True
    else:
        return

    print(error)


def invalid():
    """The finally will execute before the else returns."""
    try:
        pass
    except ValueError:
        error = None
    else:
        return
    finally:
        print(error)  # [used-before-assignment]


def invalid_2():
    """The else does not return in every branch."""
    try:
        pass
    except ValueError:
        error = None
    else:
        if range(0):
            return
    finally:
        print(error)  # [used-before-assignment]


def invalid_3():
    """Not every except defines the name."""
    try:
        pass
    except ValueError:
        error = None
    except KeyError:
        pass
    finally:
        print(error)  # [used-before-assignment]


def invalid_4():
    """Should not rely on the name in the else even if it returns."""
    try:
        pass
    except ValueError:
        error = True
    else:
        print(error)  # [used-before-assignment]
        return
