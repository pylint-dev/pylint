"""Test `no-value-for-parameter` in the context of positional-only parameters"""

# pylint: disable=missing-docstring, unused-argument


def name1(param1, /, **kwargs): ...
def name2(param1, /, param2, **kwargs): ...
def name3(param1=True, /, **kwargs): ...
def name4(param1, **kwargs): ...

name1(param1=43)  # [no-value-for-parameter]
name1(43)
name2(1, param2=False)
name3()
name4(param1=43)
