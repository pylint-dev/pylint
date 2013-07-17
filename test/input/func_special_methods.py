#pylint: disable=C0111
__revision__ = None

class ContextManager(object):
    def __enter__(self):
        pass
    def __exit__(self, *args):
        pass
    def __init__(self):
        pass

class BadContextManager(object):
    def __enter__(self):
        pass
    def __init__(self):
        pass

class Container(object):
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

class BadROContainer(object):
    def __init__(self):
        pass
    def __len__(self):
        return 0
    def __setitem__(self, key, value):
        pass
    def __iter__(self):
        pass


class BadContainer(object):
    def __init__(self):
        pass
    def __len__(self):
        return 0
    def __getitem__(self, key, value):
        pass
    def __setitem__(self, key, value):
        pass

class MyTuple(tuple):
    def __getitem__(self, index):
        return super(MyTuple, self).__getitem__(index)
