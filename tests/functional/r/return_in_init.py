# pylint: disable=missing-docstring,too-few-public-methods,useless-return

class MyClass:

    def __init__(self): # [return-in-init]
        return 1

class MyClass2:
    """dummy class"""

    def __init__(self):
        return


class MyClass3:
    """dummy class"""

    def __init__(self):
        return None

class MyClass5:
    """dummy class"""

    def __init__(self):
        self.callable = lambda: (yield None)
