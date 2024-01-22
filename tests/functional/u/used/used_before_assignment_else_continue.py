"""If the else block continues, it is generally safe to rely on assignments in the except,
inside the same for loop only."""


def safe():
    """Name used safely inside the loop."""
    while True:
        try:
            pass
        except ValueError:
            error = True
        else:
            continue

        print(error)


def halfway_safe():
    """Name used safely inside the loop, unsafely outside it."""
    for _temp in range(0, 1):
        try:
            pass
        except ValueError:
            error = True
        else:
            continue

        print(error)
    print(error)  # https://github.com/pylint-dev/pylint/issues/9379


def unsafe():
    """Name used unsafely outside the loop."""
    for _temp in range(0, 1):
        try:
            pass
        except ValueError:
            error = True
        else:
            continue

    print(error)  # [used-before-assignment]
