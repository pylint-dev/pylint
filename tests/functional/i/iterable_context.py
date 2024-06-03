"""
Checks that primitive values are not used in an
iterating/mapping context.
"""
# pylint: disable=missing-docstring,invalid-name,too-few-public-methods,import-error,unused-argument,bad-mcs-method-argument,
# pylint: disable=wrong-import-position,no-else-return, unnecessary-comprehension,redundant-u-string-prefix
# pylint: disable=use-dict-literal
# primitives
numbers = [1, 2, 3]

for i in numbers:
    pass

for i in iter(numbers):
    pass

for i in "123":
    pass

for i in u"123":
    pass

for i in b"123":
    pass

for i in bytearray(b"123"):
    pass

for i in set(numbers):
    pass

for i in frozenset(numbers):
    pass

for i in dict(a=1, b=2):
    pass

# comprehensions
for i in [x for x in range(10)]:
    pass

for i in {x for x in range(1, 100, 2)}:
    pass

for i in {x: 10 - x for x in range(10)}:
    pass

# generators
def powers_of_two():
    k = 0
    while k < 10:
        yield 2 ** k
        k += 1

for i in powers_of_two():
    pass

for i in powers_of_two:  # [not-an-iterable]
    pass

# check for custom iterators
class A:
    pass

class B:
    def __iter__(self):
        return self

    def __next__(self):
        return 1

    def next(self):
        return 1

class C:
    "old-style iterator"
    def __getitem__(self, k):
        if k > 10:
            raise IndexError
        return k + 1

    def __len__(self):
        return 10

for i in C():
    print(i)


def test(*args):
    print(args)


test(*A())  # [not-an-iterable]
test(*B())
test(*B)  # [not-an-iterable]
for i in A():  # [not-an-iterable]
    pass
for i in B():
    pass
for i in B:  # [not-an-iterable]
    pass

for i in range:  # [not-an-iterable]
    pass

# check that primitive non-iterable types are caught
for i in True:  # [not-an-iterable]
    pass

for i in None:  # [not-an-iterable]
    pass

for i in 8.5:  # [not-an-iterable]
    pass

for i in 10:  # [not-an-iterable]
    pass

# skip uninferable bases
from some_missing_module import Iterable

class MyClass(Iterable):
    pass

m = MyClass()
for i in m:
    print(i)

# skip uninferable instances
ambiguous = range(i) or range(i)
for j in ambiguous:
    print(j)

# skip checks if statement is inside mixin/base/abstract class
class ManagedAccessViewMixin:
    access_requirements = None

    def get_access_requirements(self):
        return self.access_requirements

    def dispatch(self, *_args, **_kwargs):
        classes = self.get_access_requirements()

        # no error should be emitted here
        for requirement in classes:
            print(requirement)

class BaseType:
    valid_values = None

    def validate(self, value):
        if self.valid_values is None:
            return True
        else:
            # error should not be emitted here
            for v in self.valid_values:
                if value == v:
                    return True
            return False

class AbstractUrlMarkManager:
    def __init__(self):
        self._lineparser = None
        self._init_lineparser()
        # error should not be emitted here
        for line in self._lineparser:
            print(line)

    def _init_lineparser(self):
        raise NotImplementedError

# class is not named as abstract
# but still is deduceably abstract
class UrlMarkManager:
    def __init__(self):
        self._lineparser = None
        self._init_lineparser()
        # error should not be emitted here
        for line in self._lineparser:
            print(line)

    def _init_lineparser(self):
        raise NotImplementedError


class HasDynamicGetattr:

    def __init__(self):
        self._obj = []

    def __getattr__(self, attr):
        return getattr(self._obj, attr)


for elem in HasDynamicGetattr():
    pass


# Regression test for https://github.com/pylint-dev/pylint/issues/6372
string_twos = "".join(str(*y) for _, *y in [[1, 2], [1, 2]])
