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
    print(error)  # [used-before-assignment]


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


def halfway_safe_while(cond):
    """While-loop variant: name used safely inside the loop, unsafely outside it."""
    while cond:
        try:
            pass
        except ValueError:
            result = 1
        else:
            continue

        print(result)
    print(result)  # [used-before-assignment]


def safe_defined_before_loop():
    """Name defined before the loop stays safe outside the loop."""
    error = False
    for _temp in range(0, 1):
        try:
            pass
        except ValueError:
            error = True
        else:
            continue

        print(error)
    print(error)


def safe_defined_after_loop():
    """Name unconditionally assigned after the loop before outer use stays safe."""
    for _temp in range(0, 1):
        try:
            pass
        except ValueError:
            error = True
        else:
            continue

        print(error)
    error = False
    print(error)


def two_uses_after_loop():
    """Multiple uses after the loop report once, matching unsafe()."""
    for _temp in range(0, 1):
        try:
            pass
        except ValueError:
            value = 1
        else:
            continue

        print(value)
    print(value)  # [used-before-assignment]
    print(value)


def nested_loop_outer_try():
    """Exemption from outer loop holds inside inner and outer loops, not after."""
    for _outer in range(0, 1):
        try:
            pass
        except ValueError:
            error = True
        else:
            continue

        for _inner in range(0, 1):
            print(error)
        print(error)
    print(error)  # [used-before-assignment]


def nested_loop_inner_try():
    """Exemption from inner loop does not hold in the enclosing outer loop."""
    for _outer in range(0, 1):
        for _inner in range(0, 1):
            try:
                pass
            except ValueError:
                error = True
            else:
                continue

            print(error)
        print(error)  # [used-before-assignment]
