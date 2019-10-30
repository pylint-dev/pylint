# pylint: disable=missing-docstring,too-few-public-methods
__version__ = "1.0"
ignored_SOME_CONSTANT = 42

explicit_bad_some_constant = 42  # [blacklisted-name]

snake_case_bad_SOME_CONSTANT = 42  # [invalid-name]


class my_class:
    def __init__(self, arg_x):
        self._my_secret_x = arg_x

    @property
    def my_public_x(self):
        return self._my_secret_x * 2


def blacklisted_2_snake_case():  # [blacklisted-name]
    pass
