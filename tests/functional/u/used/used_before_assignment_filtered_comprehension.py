"""Homonym between filtered comprehension and assignment in except block."""

def func():
    """https://github.com/PyCQA/pylint/issues/5586"""
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
    """https://github.com/PyCQA/pylint/issues/6035"""
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
