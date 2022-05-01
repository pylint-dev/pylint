# pylint: disable=missing-docstring,redefined-builtin, consider-using-f-string

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
