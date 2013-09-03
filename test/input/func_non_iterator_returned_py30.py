"""Check non-iterators returned by __iter__ """

# pylint: disable=too-few-public-methods

__revision__ = 0

class FirstGoodIterator(object):
    """ yields in iterator. """

    def __iter__(self):
        for index in range(10):
            yield index

class SecondGoodIterator(object):
    """ __iter__ and next """

    def __iter__(self):
        return self

    def __next__(self): # pylint: disable=no-self-use
        """ Infinite iterator, but still an iterator """
        return 1

class ThirdGoodIterator(object):
    """ Returns other iterator, not the current instance """

    def __iter__(self):
        return SecondGoodIterator()

class FourthGoodIterator(object):
    """ __iter__ returns iter(...) """

    def __iter__(self):
        return iter(range(10))

class FirstBadIterator(object):
    """ __iter__ returns a list """

    def __iter__(self):
        return []

class SecondBadIterator(object):
    """ __iter__ without next """

    def __iter__(self):
        return self

class ThirdBadIterator(object):
    """ __iter__ returns an instance of another non-iterator """

    def __iter__(self):
        return SecondBadIterator()
