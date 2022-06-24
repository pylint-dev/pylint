class Foo:
    def __init__(self, data):  # [init-is-generator]
        yield from data
