# pylint: disable=invalid-name,missing-docstring,pointless-statement,unnecessary-comprehension

var = (1, 2, 3)

for x in var:
    pass
for x in (1, 2, 3):
    pass
for x in [1, 2, 3]:  # [consider-using-tuple]
    pass

(x for x in var)
(x for x in (1, 2, 3))
(x for x in [1, 2, 3])  # [consider-using-tuple]
(x for x in {1, 2, 3})  # [consider-using-tuple]

[x for x in var]
[x for x in (1, 2, 3)]
[x for x in [1, 2, 3]]  # [consider-using-tuple]


# list/set can't be replaced if tuple unpacking is used
for x in [*var]:
    pass
for x in [2, *var]:
    pass

[x for x in [*var, 2]]
[x for x in {*var, 2}]


# -----
# Suggest tuple for `in` comparisons
x in var
x in (1, 2, 3)
x in [1, 2, 3]  # [consider-using-tuple]

if x in var:
    pass
if x in (1, 2, 3):
    pass
if x in [1, 2, 3]:  # [consider-using-tuple]
    pass
if x in {1, 2, 3}:  # [consider-using-tuple]
    pass

42 if x in [1, 2, 3] else None  # [consider-using-tuple]
assert x in [1, 2, 3]  # [consider-using-tuple]
(x for x in var if x in [1, 2, 3])  # [consider-using-tuple]
while x in [1, 2, 3]:  # [consider-using-tuple]
    break

# Stacked operators, rightmost pair is evaluated first
# Doesn't make much sense in practice since `in` will only return `bool`
True == x in [1, 2, 3]  # [consider-using-tuple]  # noqa: E712
1 >= x in [1, 2, 3]  # [consider-using-tuple]  # noqa: E712
