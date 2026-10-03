class Fruit:  # [single-string-used-for-slots]
    __slots__ = "name"

    def __init__(self, name):
        self.name = name
