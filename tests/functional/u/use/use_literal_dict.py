# pylint: disable=missing-docstring, invalid-name, disallowed-name, unused-argument, too-few-public-methods

x = dict()  # [use-dict-literal]
x = dict(a="1", b=None, c=3)  # [use-dict-literal]
x = dict(zip(["a", "b", "c"], [1, 2, 3]))
x = {}
x = {"a": 1, "b": 2, "c": 3}
x = dict(**x)  # [use-dict-literal]

def bar(boo: bool = False):
    return 1

x = dict(foo=bar())  # [use-dict-literal]

baz = {"e": 9, "f": 1}

dict(  # [use-dict-literal]
    **baz,
    suggestions=list(
        bar(
            boo=True,
        )
    ),
)

class SomeClass:
    prop: dict = {"a": 1}

inst = SomeClass()

dict(  # [use-dict-literal]
    url="/foo",
    **inst.prop,
)

dict(  # [use-dict-literal]
    Lorem="ipsum",
    dolor="sit",
    amet="consectetur",
    adipiscing="elit",
    sed="do",
    eiusmod="tempor",
    incididunt="ut",
    labore="et",
    dolore="magna",
)
