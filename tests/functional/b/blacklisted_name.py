# pylint: disable=missing-docstring

def baz(): # [blacklisted-name]
    pass

foo = {}.keys()  # [blacklisted-name]
foo = None  # [blacklisted-name]
