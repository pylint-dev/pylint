"""Check for nonlocal and used-before-assignment"""
# pylint: disable=missing-docstring, unused-variable, no-init, too-few-public-methods

__revision__ = 0

def test_ok():
    """ uses nonlocal """
    cnt = 1
    def wrap():
        nonlocal cnt
        cnt = cnt + 1
    wrap()

def test_fail():
    """ doesn't use nonlocal """
    cnt = 1
    def wrap():
        cnt = cnt + 1 # [used-before-assignment]
    wrap()

def test_fail2():
    """ use nonlocal, but for other variable """
    cnt = 1
    count = 1
    def wrap():
        nonlocal count
        cnt = cnt + 1 # [used-before-assignment]
    wrap()

def test_fail3(arg: test_fail4): # [used-before-assignment]
    """ Depends on `test_fail4`, in argument annotation. """
    return arg
# +1: [used-before-assignment, used-before-assignment]
def test_fail4(*args: test_fail5, **kwargs: undefined):
    """ Depends on `test_fail5` and `undefined` in
    variable and named arguments annotations.
    """
    return args, kwargs

def test_fail5()->undefined1: # [used-before-assignment]
    """ Depends on `undefined1` in function return annotation. """

def undefined():
    """ no op """

def undefined1():
    """ no op """


def nonlocal_in_ifexp():
    """bar"""
    bug2 = True
    def on_click(event):
        """on_click"""
        if event:
            nonlocal bug2
            bug2 = not bug2
    on_click(True)

nonlocal_in_ifexp()
