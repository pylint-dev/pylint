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

[x for x in var]
[x for x in (1, 2, 3)]
[x for x in [1, 2, 3]]  # [consider-using-tuple]


for x in [*var]:  # [consider-using-tuple]
    pass
for x in [2, *var]:  # [consider-using-tuple]
    pass

[x for x in [*var, 2]]  # [consider-using-tuple]


# Don't emit warning for sets as this is handled by builtin checker
(x for x in {1, 2, 3})  # [use-sequence-for-iteration]
[x for x in {*var, 2}]
