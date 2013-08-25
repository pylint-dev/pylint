"""Check unpacking non-sequences in assignments. """

# pylint: disable=too-few-public-methods, invalid-name

__revision__ = 0

# Working

class Seq(object):
    """ sequence """
    def __init__(self):
        self.items = range(2)

    def __getitem__(self, item):
        return self.items[item]

    def __len__(self):
        return len(self.items)

class Iter(object):
    """ Iterator """
    def __iter__(self):
        for number in range(2):
            yield number

a, b = [1, 2]
a, b = (1, 2)
a, b = set([1, 2])
a, b = {1: 2, 2: 3}
a, b =  "xy"
a, b = Seq()
a, b = Iter()
a, b = (number for number in range(2))

# Not working
class NonSeq(object):
    """ does nothing """

a, b = NonSeq()
a, b = ValueError
a, b = None
a, b = 1
a, b = locals
