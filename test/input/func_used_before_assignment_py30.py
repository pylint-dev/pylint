"""Check for nonlocal and used-before-assignment"""
# pylint: disable=missing-docstring, unused-variable

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
        cnt = cnt + 1
    wrap()

def test2_fail():
    """ uses nonlocal, but without an
    outer label defined. """
    def wrap():
        nonlocal cnt
        cnt = cnt + 1
    wrap()
