"""Test namedtuple attributes.

Regression test for:
https://bitbucket.org/logilab/pylint/issue/93/pylint-crashes-on-namedtuple-attribute
"""
__revision__ = None

from collections import namedtuple
Thing = namedtuple('Thing', ())
print Thing.x
