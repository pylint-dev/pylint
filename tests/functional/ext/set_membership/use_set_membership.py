# pylint: disable=invalid-name,missing-docstring,pointless-statement,unnecessary-comprehension,undefined-variable,bad-chained-comparison

x = 1
var = frozenset({1, 2, 3})

x in var
x in {1, 2, 3}
x in (1, 2, 3)  # [use-set-for-membership]
x in [1, 2, 3]  # [use-set-for-membership]

if x in var:
    pass
if x in {1, 2, 3}:
    pass
if x in (1, 2, 3):  # [use-set-for-membership]
    pass
if x in [1, 2, 3]:  # [use-set-for-membership]
    pass

42 if x in [1, 2, 3] else None  # [use-set-for-membership]
assert x in [1, 2, 3]  # [use-set-for-membership]
(x for x in var if x in [1, 2, 3])  # [use-set-for-membership]
while x in [1, 2, 3]:  # [use-set-for-membership]
    break

# Stacked operators, rightmost pair is evaluated first
# Doesn't make much sense in practice since `in` will only return `bool`
True == x in [1, 2, 3]  # [use-set-for-membership]  # noqa: E712
1 >= x in [1, 2, 3]  # [use-set-for-membership]  # noqa: E712


# Test hashable heuristic
x in (1, "Hello World", False, None)  # [use-set-for-membership]
x in (1, [])  # List is not hashable

if x:
    var2 = 2
else:
    var2 = []
x in (1, var2)  # var2 can be a list
