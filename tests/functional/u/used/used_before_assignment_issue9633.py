"""``if "x" not in globals(): x = ...`` defines the global ``x`` either way,
unless the body might not bind ``x`` or ``x`` is deleted.

A name only assigned in one ``if`` branch is reported the same way when it is
also bound by the statement using it (``+=``) or assigned again later on.

https://github.com/pylint-dev/pylint/issues/9633
"""
# pylint: disable=global-at-module-level, global-statement, global-variable-undefined
# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring, redefined-builtin
import contextlib
import random

# The three examples from the issue
if __name__ == "__main__":
    global g_object
    if "g_object" not in globals():
        g_object = 1
    g_object += 1

if __name__ == "__main__":
    global h_object
    if "h_object" not in globals():
        h_object = 1
    obj = h_object

if __name__ == "__main__":
    global i_object
    if "i_object" not in globals():
        i_object = 1
    obj = i_object
    i_object += 1

if "j_object" not in globals():
    j_object = 1
print(j_object)


def global_in_function():
    global k_object
    if "k_object" not in globals():
        k_object = 1
    k_object += 1


def local_in_function():
    if "value" not in globals():
        value = 1
    value += 1  # [possibly-used-before-assignment]


def globals_shadowed(globals):
    global l_object
    if "l_object" not in globals():
        l_object = 1
    l_object += 1  # [possibly-used-before-assignment]


def other_name_in_test():
    global m_object
    if "other" not in globals():
        m_object = 1
    m_object += 1  # [possibly-used-before-assignment]


def nested_condition():
    global n_object
    if "n_object" not in globals():
        if random.random():
            n_object = 1
    n_object += 1  # [possibly-used-before-assignment]


def bound_in_loop(items):
    global o_object
    if "o_object" not in globals():
        for item in items:
            o_object = item
    o_object += 1  # [possibly-used-before-assignment]


def bound_in_try():
    global p_object
    if "p_object" not in globals():
        try:
            p_object = int("x")
        except ValueError:
            pass
    p_object += 1  # [possibly-used-before-assignment]


def bound_in_with():
    global q_object
    if "q_object" not in globals():
        with contextlib.suppress(ValueError):
            q_object = int("x")
    q_object += 1  # [possibly-used-before-assignment]


def deleted_after_guard():
    global r_object
    if "r_object" not in globals():
        r_object = 1
    del r_object  # [possibly-used-before-assignment]
    return r_object


def augmented_assignment():
    if random.random():
        value = 1
    value += 1  # [possibly-used-before-assignment]
    return value


def augmented_assignment_shadowing_a_global():
    if random.random():
        j_object = 1  # pylint: disable=redefined-outer-name
    j_object += 1  # [possibly-used-before-assignment]


def read_then_reassigned():
    if random.random():
        value = 1
    print(value)  # [possibly-used-before-assignment]
    value = 2
    return value


def read_before_conditional_assignment():
    print(value)  # [used-before-assignment]
    if random.random():
        value = 1
    value = 2
    return value


def augmented_assignment_before_conditional_assignment():
    value += 1  # [undefined-variable]
    if random.random():
        value = 1
    return value


def defined_in_all_branches():
    if random.random():
        value = 1
    else:
        value = 2
    value += 1
    return value


def augmented_assignment_guarded_by_name_error():
    if random.random():
        value = 1
    try:
        value += 1
    except NameError:
        value = 0
    return value


def augmented_assignment_never_defined():
    value += 1  # [undefined-variable]
    return value


# Unchanged: the assignment is not under an ``if``
def augmented_assignment_in_except_handler():
    try:
        value = int("1")
    except ValueError:
        value += 1  # [undefined-variable]
    return value


# Unchanged: builtin names
def builtin_augmented_assignment():
    if random.random():
        list = []
    list += [1]


def builtin_read_then_reassigned():
    if random.random():
        list = []
    print(list)  # [used-before-assignment]
    list = [1]
