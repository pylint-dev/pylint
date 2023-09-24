class Student:
    __slots__ = ("name",)

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname  # [assigning-non-slot]
        self.setup()

    def setup(self):
        pass
