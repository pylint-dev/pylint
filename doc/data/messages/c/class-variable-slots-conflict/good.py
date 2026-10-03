class Person:
    __slots__ = ("_age", "name")

    def __init__(self, age, name):
        self._age = age
        self.name = name

    @property
    def age(self):
        return self._age

    def say_hi(self):
        print(f"Hi, I'm {self.name}.")
