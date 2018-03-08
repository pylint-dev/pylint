# pylint: disable=missing-docstring,invalid-name,using-constant-test

a, b, c, d = 'a b c d'.split()

temp = a # [consider-swap-variables]
a = b
b = temp

temp = a  # only simple swaps are reported
a = b
if True:
    b = a

temp = a  # this is no swap
a = b
b = a

temp = a, b  # complex swaps are ignored
a, b = c, d
c, d = temp

temp = a # [consider-swap-variables]
a = b  # longer swap circles are only reported once
b = temp
temp = a
