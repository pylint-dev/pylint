class Foo:
  def __init__(self):
    self.bar = None

X = Foo()

def function():
    X.bar = 'quux'


def entry_point(argv):
    function()
    if X.bar == 'quux':
        return 0
    return 1

def target(*args):
    return entry_point, None
