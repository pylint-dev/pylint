"""
Checks that primitive values are not used in an
iterating/mapping context.
"""
# pylint: disable=missing-docstring,invalid-name,too-few-public-methods,no-init,no-self-use
from __future__ import print_function

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
class A(object):
    pass

class B(object):
    def __iter__(self):
        return self

    def __next__(self):
        return 1

    def next(self):
        return 1

class C(object):
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

# check that primitive non-iterable types are catched
for i in True:  # [not-an-iterable]
    pass

for i in None:  # [not-an-iterable]
    pass

for i in 8.5:  # [not-an-iterable]
    pass

for i in 10:  # [not-an-iterable]
    pass
