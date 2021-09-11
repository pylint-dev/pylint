# pylint: disable=missing-docstring,pointless-statement,unnecessary-comprehension

var = {1, 2, 3}

for x in var:
    pass
for x in {1, 2, 3}:  # [use-sequence-for-iteration]
    pass

(x for x in var)
(x for x in {1, 2, 3})  # [use-sequence-for-iteration]

[x for x in var]
[x for x in {1, 2, 3}]  # [use-sequence-for-iteration]

[x for x in {*var, 4}]  # [use-sequence-for-iteration]
