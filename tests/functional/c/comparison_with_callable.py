# pylint: disable = disallowed-name, missing-docstring, useless-return, invalid-name, line-too-long, comparison-of-constants, broad-exception-raised
def foo():
    return None

def goo():
    return None

if foo == 786:  # [comparison-with-callable]
    pass

if 666 == goo:  # [comparison-with-callable]
    pass

if foo == goo:
    pass

if foo() == goo():
    pass


class FakeClass:
    def __init__(self):
        self._fake_prop = 'fake it till you make it!!'

    def fake_method(self):
        return '666 - The Number of the Beast'

    @property
    def fake_property(self):
        return self._fake_prop

    @fake_property.setter
    def fake_property(self, prop):
        self._fake_prop = prop

obj1 = FakeClass()
obj2 = FakeClass()

if obj1.fake_method == obj2.fake_method:
    pass

if obj1.fake_property != obj2.fake_property:    # property although is function but is called without parenthesis
    pass

if obj1.fake_method != foo:
    pass

if obj1.fake_method != 786: # [comparison-with-callable]
    pass

if obj1.fake_method != obj2.fake_property: # [comparison-with-callable]
    pass

if 666 == 786:
    pass

a = 666
b = 786
if a == b:
    pass


def eventually_raise():
    print()
    raise Exception


if a == eventually_raise:
    # Does not emit comparison-with-callable because the
    # function (eventually) raises
    pass
