# pylint: disable=missing-docstring,redefined-builtin, consider-using-f-string, unnecessary-direct-lambda-call, broad-exception-raised

import sys

if sys.version_info >= (3, 8):
    from typing import NoReturn
else:
    from typing_extensions import NoReturn


def do_stuff(some_random_list):
    for var in some_random_list:
        pass
    return var # [undefined-loop-variable]


def do_else(some_random_list):
    for var in some_random_list:
        if var == 42:
            break
    else:
        var = 84
    return var

__revision__ = 'yo'

TEST_LC = [C for C in __revision__ if C.isalpha()]
B = [B for B in  __revision__ if B.isalpha()]
VAR2 = B # nor this one

for var1, var2 in TEST_LC:
    var1 = var2 + 4
VAR3 = var1 # [undefined-loop-variable]

for note in __revision__:
    note.something()
for line in __revision__:
    for note in line:
        A = note.anotherthing()


for x in []:
    pass
for x in range(3):
    VAR5 = (lambda: x)()


def do_stuff_with_a_list():
    for var in [1, 2, 3]:
        pass
    return var


def do_stuff_with_a_set():
    for var in {1, 2, 3}:  # pylint: disable=use-sequence-for-iteration
        pass
    return var


def do_stuff_with_a_dict():
    for var in {1: 2, 3: 4}:
        pass
    return var


def do_stuff_with_a_tuple():
    for var in (1, 2, 3):
        pass
    return var


def do_stuff_with_a_range():
    for var in range(1, 2):
        pass
    return var


def do_stuff_with_redefined_range():
    def range(key):
        yield from [1, key]
    for var in range(3):
        pass
    return var # [undefined-loop-variable]


def test(content):
    # https://github.com/PyCQA/pylint/issues/3711
    def handle_line(layne):
        if "X" in layne:
            layne = layne.replace("X", "Y")
        elif "Y" in layne:  # line 5
            layne = '{}'.format(layne)
        elif "Z" in layne:  # line 7
            layne = f'{layne}'
        else:
            layne = '%s' % layne  # line 10

    for layne in content.split('\n'):
        handle_line(layne)


def for_else_returns(iterable):
    for thing in iterable:
        break
    else:
        return
    print(thing)


def for_else_raises(iterable):
    for thing in iterable:
        break
    else:
        raise Exception
    print(thing)


def for_else_break(iterable):
    while True:
        for thing in iterable:
            break
        else:
            break
        print(thing)


def for_else_continue(iterable):
    while True:
        for thing in iterable:
            break
        else:
            continue
        print(thing)


def for_else_no_return(iterable):
    def fail() -> NoReturn:
        ...

    while True:
        for thing in iterable:
            break
        else:
            fail()
        print(thing)


lst = []
lst2 = [1, 2, 3]

for item in lst:
    pass

bigger = [
    [
        x for x in lst2 if x > item
    ]
    for item in lst
]


def lambda_in_first_of_two_loops():
    """https://github.com/PyCQA/pylint/issues/6419"""
    my_list = []
    for thing in my_list:
        print_it = lambda: print(thing)  # pylint: disable=cell-var-from-loop, unnecessary-lambda-assignment
        print_it()

    for thing in my_list:
        print(thing)


def variable_name_assigned_in_body_of_second_loop():
    for alias in tuple(bigger):
        continue
    for _ in range(3):
        alias = True
        if alias:
            print(alias)


def use_enumerate():
    """https://github.com/PyCQA/pylint/issues/6593"""
    for i, num in enumerate(range(3)):
        pass
    print(i, num)


def use_enumerate_in_ternary_expression():
    """https://github.com/PyCQA/pylint/issues/7131"""
    for i, num in enumerate(range(3)) if __revision__ else enumerate(range(4)):
        pass
    print(i, num)


def find_even_number(container):
    """https://github.com/PyCQA/pylint/pull/6923#discussion_r895134495"""
    for something in container:
        if something % 2 == 0:
            break
    return something  # [undefined-loop-variable]
