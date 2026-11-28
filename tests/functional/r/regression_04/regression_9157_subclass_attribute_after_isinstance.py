"""Regression test for https://github.com/pylint-dev/pylint/issues/9157

A function annotated to return the parent class returns the subclass here.
After ``assert isinstance(obj, Child)``, setting an attribute that
``Child.__init__`` defines is not defining one outside ``__init__``. Fixed in
astroid by pylint-dev/astroid#3387.
"""

# pylint: disable=missing-docstring,too-few-public-methods


class Parent:
    def __init__(self):
        pass


class Child(Parent):
    def __init__(self):
        super().__init__()
        self.some_value = 0


def get_parent(child: bool) -> Parent:
    if child:
        return Child()
    return Parent()


obj = get_parent(True)
assert isinstance(obj, Child)
obj.some_value = 27
