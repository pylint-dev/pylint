"""Accessing a protected method through super() is ok."""

# pylint: disable=missing-docstring,too-few-public-methods, print-statement

__revision__ = None

class Alpha(object):

    _secret = 2

    def test(self):
        print "test %s" % self


class Beta(Alpha):

    def test(self):
        print super(Beta, self)._secret
        super(Beta, self).test()


Beta().test()
