"""Test that boolean conditions can be simplified"""
# pylint: disable=pointless-statement


def func(_):
    """Pointless function"""


CONSTANT = 100
OTHER = 200

# Simplifies any boolean expression that is coerced into a True/False value
bool(CONSTANT or False)  # [simplifiable-condition]
assert CONSTANT or False  # [simplifiable-condition]
if CONSTANT and True:  # [simplifiable-condition]
    pass
elif CONSTANT and True:  # [simplifiable-condition]
    pass
while CONSTANT and True:  # [simplifiable-condition]
    break
1 if CONSTANT or False else 2  # [simplifiable-condition]
z = [x for x in range(10) if x or False]  # [simplifiable-condition]

# Simplifies recursively
assert CONSTANT or (True and False)  # [simplifiable-condition]
assert True and CONSTANT and OTHER  # [simplifiable-condition]
assert (CONSTANT or False) and (OTHER or True)  # [simplifiable-condition]

# Will try to infer the truthiness of an expression as long as it doesn't contain any variables
assert [] or CONSTANT  # [simplifiable-condition]
assert {} or CONSTANT  # [simplifiable-condition]

# Expressions not in one of the above situations will not emit a message
CONSTANT or True
bool(CONSTANT or OTHER)
bool(func(CONSTANT or True))

# https://www.reddit.com/r/learnpython/comments/y5vtrw/confused_on_pylint_message_simplifiablecondition/
board = {}
if "wking" and "bking" in board.values():  # [simplifiable-condition]
    pass
