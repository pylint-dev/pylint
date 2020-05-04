class Foo:
    pass


class Bar(Foo):
    def __init__(self):
        super(Bar, self).__init__()  # [old-style-super]


class Baz(Foo):
    def __init__(self):
        super().__init__()


class Qux(Foo):
    def __init__(self):
        super(Bar, self).__init__()
