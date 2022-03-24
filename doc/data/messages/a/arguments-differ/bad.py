class Foo:
    def bar(self, arg):
        pass


class Baz(Foo):
    def bar(self, arg, arg2):  # [arguments-differ]
        pass
