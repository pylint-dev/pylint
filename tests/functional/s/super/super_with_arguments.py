class Foo:
    pass


class Bar(Foo):
    def __init__(self):
        super(Bar, self).__init__()  # [super-with-arguments]


class Baz(Foo):
    def __init__(self):
        super().__init__()


class Qux(Foo):
    def __init__(self):
        super(Bar, self).__init__()


class NotSuperCall(Foo):
    def __init__(self):
        super.test(Bar, self).__init__()


class InvalidSuperCall(Foo):
    def __init__(self):
        super(InvalidSuperCall.__class__, self).__init__()


def method_accepting_cls(cls, self):
    # Using plain `super()` is not valid here, since there's no `__class__` cell found
    # (Exact exception would be 'RuntimeError: super(): __class__ cell not found')
    # Instead, we expect to *not* see a warning about `super-with-arguments`.
    # Explicitly passing `cls`, and `self` to `super()` is what's required.
    super(cls, self).__init__()
