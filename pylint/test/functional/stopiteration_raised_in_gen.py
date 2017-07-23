# pylint: disable=missing-docstring,invalid-name
def gen1():
    yield 1
    yield 2
    yield 3
    raise StopIteration  # [stopiteration-raised-in-gen]


def gen2():
    g = gen1()
    while True:
        yield next(g)  # [stopiteration-raised-in-gen]


def gen3():
    g = gen1()
    while True:
        try:
            yield next(g)
        except StopIteration:
            return


def gen4():
    for el in gen2():
        yield el
