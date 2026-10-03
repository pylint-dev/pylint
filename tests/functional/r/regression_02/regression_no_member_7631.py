"""Regression test from https://github.com/pylint-dev/pylint/issues/7631
The following code should NOT raise no-member.
"""
# pylint: disable=missing-docstring,too-few-public-methods

class Base:
    attr: int = 2

class Parent(Base):
    attr: int

class Child(Parent):
    attr = 2

    def __init__(self):
        self.attr = self.attr | 4
