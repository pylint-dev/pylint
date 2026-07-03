"""
Ensure that also decorator calls caught correctly
Column and line not correctly detected with Python 3.8, so we
skip it and only test versions after that.
"""


def decoractor_func(*args, **kwargs):
    """A docstring"""
    return lambda x: f"Foobar {args} {kwargs}"


@decoractor_func(
    aaaaaaaaaaaaaaaaaaalllllllooooooooooooonnngggggggggglllline=1,
    normal=2,
    fåling=3,  # [non-ascii-name]
)
def a_function():
    """A docstring"""
