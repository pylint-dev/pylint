class Person:
    __slots__ = ("age", "name", "say_hi",)  # [class-variable-slots-conflict, class-variable-slots-conflict, class-variable-slots-conflict]
    name = None

    def __init__(self, age, name):
        self.name = name
        self.age = age

    @property
    def age(self):
        return self.age

    def say_hi(self):
        print(f"Hi, I'm {self.name}.")
