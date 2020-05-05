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
