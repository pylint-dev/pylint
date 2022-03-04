"""Using non ascii variables in local"""


def okay():
    """docstring"""
    łol = "foo"  # [non-ascii-name]
    # Usage should not raise a second error
    baring = łol
    print(baring)
