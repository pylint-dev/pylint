"""
Checks that primitive values are not used in an
iterating/mapping context.
"""
# pylint: disable=missing-docstring,invalid-name
from __future__ import print_function

# for-statement
for i in 42:  # [not-an-iterable]
    pass

for i in True:  # [not-an-iterable]
    pass

# funcall-starargs
def test(*args, **kwargs):
    print(args, kwargs)

test(*1)  # [not-an-iterable]
test(*False)  # [not-an-iterable]

# funcall-kwargs
test(**1)  # [not-a-mapping]
test(**None)  # [not-a-mapping]

# list-comprehension
test([3 ** x for x in 10])  # [not-an-iterable]

# dict-comprehension
test({k: chr(k) for k in 128})  # [not-an-iterable]

# set-comprehension
test({x for x in 32})  # [not-an-iterable]

# generator-expression
test(str(x) for x in 10)  # [not-an-iterable]
