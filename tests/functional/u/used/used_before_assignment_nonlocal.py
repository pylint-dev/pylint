"""Check for nonlocal and used-before-assignment"""
# pylint: disable=missing-docstring, unused-variable, too-few-public-methods


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


def type_annotation_only_gets_value_via_nonlocal():
    """https://github.com/pylint-dev/pylint/issues/5394"""
    some_num: int
    def inner():
        nonlocal some_num
        some_num = 5
    inner()
    print(some_num)


def type_annotation_only_gets_value_via_nonlocal_nested():
    """Similar, with nesting"""
    some_num: int
    def inner():
        def inner2():
            nonlocal some_num
            some_num = 5
        inner2()
    inner()
    print(some_num)


def type_annotation_never_gets_value_despite_nonlocal():
    """Type annotation lacks a value despite nonlocal declaration"""
    some_num: int
    def inner():
        nonlocal some_num
    inner()
    print(some_num)  # [used-before-assignment]


def inner_function_lacks_access_to_outer_args(args):
    """Check homonym between inner function and outer function names"""
    def inner():
        print(args)  # [used-before-assignment]
        args = []
    inner()
    print(args)


def inner_function_ok(args):
    """Explicitly redefined homonym defined before is OK."""
    def inner():
        args = []
        print(args)
    inner()
    print(args)
