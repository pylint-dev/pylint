# pylint: disable=R0903
"""test __init__ return
"""

__revision__ = 'yo'

class MyClass:
    """dummy class"""

    def __init__(self):
        return 1

class MyClass2:
    """dummy class"""

    def __init__(self):
        return

class MyClass3:
    """dummy class"""

    def __init__(self):
        return None

class MyClass4:
    """dummy class"""

    def __init__(self):
        yield None
