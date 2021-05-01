# pylint: disable=missing-docstring,pointless-statement,invalid-name,too-few-public-methods

class A:
    @property
    def value(self):
        return 42


a = A()
a.value()  # [not-callable]
