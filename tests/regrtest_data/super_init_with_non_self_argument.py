"""
https://github.com/pylint-dev/pylint/issues/9519
"""

# pylint: disable=missing-class-docstring,missing-function-docstring,too-few-public-methods
class Window:
    def print_text(self, txt):
        print(f'{__class__} {txt}')


class Win(Window):
    def __init__(self, txt):
        super().__init__(txt)

Win('hello')
