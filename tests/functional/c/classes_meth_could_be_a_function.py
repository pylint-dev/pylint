# pylint: disable=missing-docstring,too-few-public-methods,useless-object-inheritance
"""
#2479

R0201 (formerly W0212), Method could be a function shouldn't be emitted in case
like factory method pattern
"""
__revision__ = 1

class XAsub(object):
    pass
class XBsub(XAsub):
    pass
class XCsub(XAsub):
    pass

class Aimpl(object):
    # disable "method could be a function" on classes which are not overriding
    # the factory method because in that case the usage of polymorphism is not
    # detected
    # pylint: disable=no-self-use
    def makex(self):
        return XAsub()

class Bimpl(Aimpl):

    def makex(self):
        return XBsub()

class Cimpl(Aimpl):

    def makex(self):
        return XCsub()
