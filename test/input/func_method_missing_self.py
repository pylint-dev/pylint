"""Checks that missing self in method defs don't crash Pylint !
"""

__revision__ = ''


class MyClass:
    """SimpleClass
    """

    def __init__(self):
        self.var = "var"

    def met():
        """Checks that missing self dont crash Pylint !
        """

    def correct(self):
        """yo"""
        self.var = "correct"

if __name__ == '__main__':
    OBJ = MyClass()

