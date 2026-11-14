"""Names bound by ``except ... as name:`` are deleted when the handler ends.

https://github.com/pylint-dev/pylint/issues/157
"""
# pylint: disable=missing-function-docstring, invalid-name, broad-exception-caught


def shadowed_by_handler_name():
    exc = None
    print(exc)
    try:
        print(1 / 0)
    except ZeroDivisionError as exc:
        print(exc)
    if exc is not None:  # [possibly-used-before-assignment]
        raise exc  # [possibly-used-before-assignment]


def used_in_and_after_handler():
    try:
        print(1 / 0)
    except ZeroDivisionError as err:
        print(err)
    print(err)  # [used-before-assignment]


def rebound_after_handler():
    err = None
    print(err)
    try:
        print(1 / 0)
    except ZeroDivisionError as err:
        print(err)
    err = None
    print(err)


def handler_exits():
    err = None
    print(err)
    try:
        print(1 / 0)
    except ZeroDivisionError as err:
        print(err)
        raise
    print(err)


def use_in_other_branch(flag):
    err = None
    if flag:
        try:
            print(1 / 0)
        except ZeroDivisionError as err:
            print(err)
    else:
        print(err)


def use_in_nested_function():
    try:
        print(1 / 0)
    except ZeroDivisionError as err:
        print(err)

    def inner():
        print(err)

    return inner


def use_in_later_handler_with_same_name():
    try:
        print(1 / 0)
    except ZeroDivisionError as err:
        print(err)
    try:
        print(1 / 0)
    except ZeroDivisionError as err:
        print(err)


def two_handlers_then_use():
    try:
        print(1 / 0)
    except ZeroDivisionError as err:
        print(err)
    try:
        print(1 / 0)
    except ZeroDivisionError as err:
        print(err)
    print(err)  # [used-before-assignment]
