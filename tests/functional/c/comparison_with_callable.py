# pylint: disable = blacklisted-name, missing-docstring, useless-return, misplaced-comparison-constant, invalid-name, no-self-use, line-too-long, useless-object-inheritance
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


class FakeClass(object):
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
