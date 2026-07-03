# pylint: disable=missing-docstring,too-few-public-methods

def baz():  # [disallowed-name]
    pass

class foo():  # [disallowed-name]
    pass

foo = {}.keys()  # Should raise disallowed-name once _check_name() is refactored.
foo = 42  # [disallowed-name]
aaa = 42  # [invalid-name]
