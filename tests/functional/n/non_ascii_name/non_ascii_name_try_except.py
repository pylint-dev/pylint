"""
Also variables defined in except can't contain non ascii chars
"""


try:
    raise AttributeError("Test")
    # +1: [non-ascii-identifier]
except AttributeError as łol:
    # Usage should not raise a second error
    foo = łol
