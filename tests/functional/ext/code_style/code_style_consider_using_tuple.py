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
