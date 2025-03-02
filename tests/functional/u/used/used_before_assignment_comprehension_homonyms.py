"""Homonym between filtered comprehension and assignment in except block."""
# pylint: disable=broad-exception-raised

def func():
    """https://github.com/pylint-dev/pylint/issues/5586"""
    try:
        print(value for value in range(1 / 0) if isinstance(value, int))
    except ZeroDivisionError:
        value = 1
        print(value)


def func2():
    """Same, but with attribute access."""
    try:
        print(value for value in range(1 / 0) if isinstance(value.num, int))
    except ZeroDivisionError:
        value = 1
        print(value)


def func3():
    """Same, but with no call."""
    try:
        print(value for value in range(1 / 0) if value)
    except ZeroDivisionError:
        value = 1
        print(value)


def func4():
    """https://github.com/pylint-dev/pylint/issues/6035"""
    assets = [asset for asset in range(3) if asset.name == "filename"]

    try:
        raise ValueError
    except ValueError:
        asset = assets[0]
        print(asset)


def func5():
    """Similar, but with subscript notation"""
    results = {}
    # pylint: disable-next=consider-using-dict-items
    filtered =  [k for k in results if isinstance(results[k], dict)]

    try:
        1 / 0
    except ZeroDivisionError:
        k = None
        print(k, filtered)


def func6(data, keys):
    """Similar, but with a subscript in a key-value pair rather than the test
    See https://github.com/pylint-dev/pylint/issues/6069"""
    try:
        results = {key: data[key] for key in keys}
    except KeyError as exc:
        key, *_ = exc.args
        raise Exception(f"{key} not found") from exc

    return results


def func7():
    """Similar, but with a comparison"""
    bools = [str(i) == i for i in range(3)]

    try:
        1 / 0
    except ZeroDivisionError:
        i = None
        print(i, bools)


def func8():
    """Similar, but with a container"""
    pairs = [(i, i) for i in range(3)]

    try:
        1 / 0
    except ZeroDivisionError:
        i = None
        print(i, pairs)


# Module level cases

module_ints = [j | j for j in range(3)]
try:
    1 / 0
except ZeroDivisionError:
    j = None
    print(j, module_ints)
