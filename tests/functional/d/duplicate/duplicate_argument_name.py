"""Check for duplicate function arguments."""

# pylint: disable=missing-docstring, line-too-long


def foo1(_, _): # [duplicate-argument-name]
    ...

def foo2(_abc, *, _abc): # [duplicate-argument-name]
    ...

def foo3(_, _=3): # [duplicate-argument-name]
    ...

def foo4(_, *, _): # [duplicate-argument-name]
    ...

def foo5(_, *_, _=3): # [duplicate-argument-name, duplicate-argument-name]
    ...

# +1: [duplicate-argument-name, duplicate-argument-name, duplicate-argument-name, duplicate-argument-name]
def foo6(_, /, _, *_, _="_", **_):
    ...
