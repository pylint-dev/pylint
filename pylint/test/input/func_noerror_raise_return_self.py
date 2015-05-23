"""see ticket #5672"""
# pylint: disable=R0903,W0232,C0111,C0103,using-constant-test

__revision__ = 0

class MultiException(Exception):
    def __init__(self):
        Exception.__init__(self)
    def return_self(self):
        return self

# raise Exception
if 1:
    raise MultiException().return_self()

