import random

# +1: [using-assignment-expression-in-unsupported-version]
if zero_or_one := random.randint(0, 1):
    assert zero_or_one == 1
