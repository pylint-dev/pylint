"""pylint should detect yield and return mix inside generators"""
# pylint: disable=using-constant-test, inconsistent-return-statements
def somegen():
    """this is a bad generator"""
    if True:
        return 1
    else:
        yield 2

def moregen():
    """this is another bad generator"""
    if True:
        yield 1
    else:
        return 2
