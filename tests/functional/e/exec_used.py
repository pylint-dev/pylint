# pylint: disable=missing-docstring

exec('a = 42') # [exec-used]
exec('a = 1', globals={}) # [exec-used]

exec('a = 1', globals=globals()) # [exec-used]

def func():
    exec('b = 1') # [exec-used]
