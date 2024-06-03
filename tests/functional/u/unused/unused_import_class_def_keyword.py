"""
Test false-positive for unused-import on class keyword arguments

    https://github.com/pylint-dev/pylint/issues/3202
"""
# pylint: disable=missing-docstring,too-few-public-methods,invalid-name,import-error

# Imports don't exist! Only check `unused-import`
from const import DOMAIN
from const import DOMAIN_2
from const import DOMAIN_3


class Child:
    def __init_subclass__(cls, **kwargs):
        pass

class Parent(Child, domain=DOMAIN):
    pass


# Alternative 1
class Parent_2(Child, domain=DOMAIN_2):
    DOMAIN_2 = DOMAIN_2


# Alternative 2
class A:
    def __init__(self, arg):
        pass

class B:
    CONF = "Hello World"
    SCHEMA = A(arg=CONF)


# Test normal instantiation
A(arg=DOMAIN_3)
