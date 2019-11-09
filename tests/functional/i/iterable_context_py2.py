"""
Checks that iterable metaclasses are recognized by pylint.
"""
# pylint: disable=missing-docstring,too-few-public-methods,no-init,no-self-use,unused-argument,bad-mcs-method-argument, useless-object-inheritance

# metaclasses as iterables
class Meta(type):
    def __iter__(self):
        return iter((1, 2, 3))

class SomeClass(object):
    __metaclass__ = Meta


for i in SomeClass:
    print i
for i in SomeClass():  # [not-an-iterable]
    print i
