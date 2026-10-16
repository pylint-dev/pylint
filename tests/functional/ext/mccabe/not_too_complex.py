"""The other functional file has a max-complexity so low that it doesn't cover the
 case when the code is not too complex."""


def not_too_complex():
    """McCabe rating: 1"""
    return True


def too_complex(condition):  # [too-complex]
    """McCabe rating: 2"""
    if condition is True:
        return True
    return False
