# pylint: disable=missing-docstring, invalid-name

x = list()  # [use-list-literal]
x = list("string")
x = list(range(3))
x = []
x = ["string"]
x = [1, 2, 3]
x = [range(3)]
x = list(**{})
x = [].copy()


def shadowed_by_a_class():
    list = tuple  # pylint: disable=redefined-builtin
    return list()


def shadowed_by_a_function():
    list = lambda: []  # pylint: disable=redefined-builtin, unnecessary-lambda-assignment
    return list()
