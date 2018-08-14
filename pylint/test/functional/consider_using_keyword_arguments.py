# pylint: disable=missing-docstring, invalid-name

def func(*args):
    return args

func(1, 2, 3)

func(*(1, 2, 3, 4, 5))

func(1, 2, 3, 4, 5) # [consider-using-keyword-arguments]
