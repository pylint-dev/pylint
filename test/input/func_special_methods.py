#pylint: disable=C0111
__revision__ = None

class ContextManager:
    def __enter__(self):
        pass
    def __exit__(self, *args):
        pass
    def __init__(self):
        pass

class BadContextManager:
    def __enter__(self):
        pass
    def __init__(self):
        pass

class Container:
    def __init__(self):
        pass
    def __len__(self):
        return 0
    def __getitem__(self, key):
        pass
    def __setitem__(self, key, value):
        pass
    def __delitem__(self, key, value):
        pass
    def __iter__(self):
        pass

class BadContainer:
    def __init__(self):
        pass
    def __len__(self):
        return 0
    def __setitem__(self, key, value):
        pass
    def __iter__(self):
        pass

class Callable:
    def __call__(self):
        pass
    def __init__(self):
        pass

