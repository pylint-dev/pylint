class Foo:
    def __init__(self, data):
        self.data = data

    def get_items(self):
        yield from self.data

foo = Foo([1, 2, 3])
for item in foo.get_items():
    pass
