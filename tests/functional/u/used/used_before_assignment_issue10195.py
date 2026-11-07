"""A later assignment must not turn a possibly-unbound name into a definitely
unbound one.
See https://github.com/pylint-dev/pylint/issues/10195"""
# pylint: disable=missing-function-docstring


def assigned_again_in_else(x):
    if x != 0:
        v = None
    if x == 1:
        print(v)  # [possibly-used-before-assignment]
    else:
        v = None


def assigned_again_after_use(cond, n):
    if cond:
        v = 2
    print(v)  # [possibly-used-before-assignment]
    v = n
    return v


def assigned_again_by_walrus(cond, n):
    if cond:
        v = 2
    print(v)  # [possibly-used-before-assignment]
    if (v := n + 1) > 0:
        print(v)


def conditional_assignment_comes_after_use(cond):
    print(v)  # [used-before-assignment]
    if cond:
        v = 1
    v = 2
    return v


def assigned_in_same_handler(text):
    try:
        v = int(text)
    except ValueError:
        print(v)  # [used-before-assignment]
        v = 0
    return v


def shadowed_builtin_assigned_again(cond):
    if cond:
        len = print  # pylint: disable=redefined-builtin
    print(len)  # [used-before-assignment]
    len = 3  # pylint: disable=redefined-builtin
    return len
