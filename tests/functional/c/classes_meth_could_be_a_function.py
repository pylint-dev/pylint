# pylint: disable=missing-docstring,too-few-public-methods
"""
#2479

R0201 (formerly W0212), Method could be a function shouldn't be emitted in case
like factory method pattern
"""


class XAsub:
    pass
class XBsub(XAsub):
    pass
class XCsub(XAsub):
    pass

class Aimpl:
    # disable "method could be a function" on classes which are not overriding
    # the factory method because in that case the usage of polymorphism is not
    # detected
    def makex(self):
        return XAsub()

class Bimpl(Aimpl):

    def makex(self):
        return XBsub()

class Cimpl(Aimpl):

    def makex(self):
        return XCsub()
