"""
Checks that primitive values are not used in an
iterating/mapping context.
"""
# pylint: disable=missing-docstring,invalid-name,too-few-public-methods,no-init
from __future__ import print_function

# for-statement
for i in 42:  # [not-an-iterable]
    pass

for i in True:  # [not-an-iterable]
    pass

for i in range(10):
    pass

for i in ''.join(x ** 2 for x in range(10)):
    pass

numbers = [1, 2, 3]
inumbers = iter(numbers)

for i in inumbers:
    pass

for i in "123":
    pass

for i in u"123":
    pass

for i in set(numbers):
    pass

for i in frozenset(numbers):
    pass

for i in dict(a=1, b=2):
    pass

for i in [x for x in range(10)]:
    pass

for i in {x for x in range(1, 100, 2)}:
    pass

for i in {x: 10 - x for x in range(10)}:
    pass

def powers_of_two():
    k = 0
    while k < 10:
        yield 2 ** k
        k += 1

for i in powers_of_two():
    pass


# check for old-style iterator
class C(object):
    def __getitem__(self, k):
        if k > 10:
            raise IndexError
        return k + 1

    def __len__(self):
        return 10

for i in C():
    print(i)


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


def test(*args):
    pass


test(*A())  # [not-an-iterable]
test(*B())
for i in A():  # [not-an-iterable]
    pass
