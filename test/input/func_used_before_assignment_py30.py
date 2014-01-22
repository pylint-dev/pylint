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

def test_fail2():
    """ use nonlocal, but for other variable """
    cnt = 1
    count = 1
    def wrap():
        nonlocal count
        cnt = cnt + 1
    wrap()
