# pylint: disable=C
def foo():
    _dispatch = {}

    def save(fn):
        _dispatch[fn.__name__] = fn
        return fn

    @save
    def bar():
        ...
    # do whatever
foo()
