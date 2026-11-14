"""Function parameters shadow the iterators of the enclosing scopes."""

# pylint: disable=missing-docstring,invalid-name,redefined-outer-name

rows = map(str.split, ["a b", "c d"])


def module_iterator_shadowed_by_parameter(rows, columns):
    # ``rows`` is the parameter here, not the module-level iterator.
    for column in columns:
        for row in rows:
            print(column, row)


def iterator_shadowed_by_nested_function_parameters(data):
    items = iter(data)
    args = map(str, data)
    kwargs = filter(None, data)

    def show(*args, items, **kwargs):
        for _i in range(2):
            for item in items:
                print(item)
            for arg in args:
                print(arg)
            for key in kwargs:
                print(key)

    show(1, items=[1], key=2)
    return items, args, kwargs


def parameter_rebound_to_iterator_warns(rows, columns):
    rows = iter(rows)
    for column in columns:
        for row in rows:  # [looping-through-iterator]
            print(column, row)
