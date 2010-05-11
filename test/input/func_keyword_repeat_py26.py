"""Test repeated keyword argument checker"""
__revision__ = ''

def function_default_arg(one=1, two=2):
    """fonction with default value"""
    return two, one

function_default_arg(two=5, two=7)
function_default_arg(two=5, one=7, one='bob')


