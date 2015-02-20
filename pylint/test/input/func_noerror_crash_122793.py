# pylint: disable=C0121
"""https://www.logilab.org/ticket/122793"""

def gen():
    """dumb generator"""
    yield

GEN = gen()
next(GEN)
