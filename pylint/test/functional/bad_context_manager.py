"""Check that __exit__ special method accepts 3 arguments """

# pylint: disable=too-few-public-methods, invalid-name

__revision__ = 0

class FirstGoodContextManager(object):
    """ 3 arguments """

    def __enter__(self):
        return self

    def __exit__(self, exc_type, value, tb):
        pass

class SecondGoodContextManager(object):
    """ 3 keyword arguments """

    def __enter__(self):
        return self

    def __exit__(self, exc_type=None, value=None, tb=None):
        pass

class ThirdGoodContextManager(object):
    """ 1 argument and variable arguments """

    def __enter__(self):
        return self

    def __exit__(self, exc_type, *args):
        pass

class FirstBadContextManager(object):
    """ 1 argument """

    def __enter__(self):
        return self

    def __exit__(self, exc_type): # [bad-context-manager]
        pass

class SecondBadContextManager(object):
    """ Too many arguments """

    def __enter__(self):
        return self

    def __exit__(self, exc_type, value, tb, stack): # [bad-context-manager]
        pass

class ThirdBadContextManager(object):
    """ Too many arguments and variable arguments """

    def __enter__(self):
        return self

    # +1: [bad-context-manager]
    def __exit__(self, exc_type, value, tb, stack, *args):
        pass
