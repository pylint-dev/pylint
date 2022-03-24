class Foo:
    def bar(self, arg):
        pass


class Baz:
    def __init__(self, intermediate):
        self.intermediate = intermediate

    def bar(self, arg):
        args = [arg, *self.intermediate]
