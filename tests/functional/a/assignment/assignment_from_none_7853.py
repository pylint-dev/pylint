"""
Check False positive issue #7853
"""
# pylint: disable=missing-function-docstring


def get_func(param):
    if param is None:
        def func():
            return None
    else:
        def func():
            return param
    return func


def process_val(param):

    func_a = get_func(param)
    val = func_a()
    # Do stuff with 'val'; *None* is an useful case.
    return val
