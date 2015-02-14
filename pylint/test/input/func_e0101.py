# pylint: disable=R0903
"""test __init__ return
"""

__revision__ = 'yo'

class MyClass(object):
    """dummy class"""

    def __init__(self):
        return 1

class MyClass2(object):
    """dummy class"""

    def __init__(self):
        return

class MyClass3(object):
    """dummy class"""

    def __init__(self):
        return None

class MyClass4(object):
    """dummy class"""

    def __init__(self):
        yield None

class MyClass5(object):
    """dummy class"""

    def __init__(self):
        self.callable = lambda: (yield None)
