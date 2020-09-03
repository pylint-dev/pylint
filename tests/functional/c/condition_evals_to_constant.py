"""Test that boolean conditions simplify to a constant value"""
# pylint: disable=pointless-statement
from unknown import Unknown  # pylint: disable=import-error


def func(_):
    """Pointless function"""


CONSTANT = 100
OTHER = 200

# Simplifies any boolean expression that is coerced into a True/False value
bool(CONSTANT or True)  # [condition-evals-to-constant]
assert CONSTANT or True  # [condition-evals-to-constant]
if CONSTANT and False:  # [condition-evals-to-constant]
    pass
elif CONSTANT and False:  # [condition-evals-to-constant]
    pass
while CONSTANT and False:  # [condition-evals-to-constant]
    break
1 if CONSTANT or True else 2  # [condition-evals-to-constant]
z = [x for x in range(10) if x or True]  # [condition-evals-to-constant]

# Simplifies recursively
assert True or CONSTANT or OTHER  # [condition-evals-to-constant]
assert (CONSTANT or True) or (CONSTANT or True)  # [condition-evals-to-constant]

# Will try to infer the truthiness of an expression as long as it doesn't contain any variables
assert 3 + 4 or CONSTANT  # [condition-evals-to-constant]
assert Unknown or True  # [condition-evals-to-constant]

assert True or True  # [condition-evals-to-constant]
assert False or False  # [condition-evals-to-constant]
assert True and True  # [condition-evals-to-constant]
assert False and False  # [condition-evals-to-constant]


# A bare constant that's not inside of a boolean operation will emit `using-constant-test` instead
if True:  # pylint: disable=using-constant-test
    pass

# Expressions not in one of the above situations will not emit a message
CONSTANT or True
bool(CONSTANT or OTHER)
bool(func(CONSTANT or True))
