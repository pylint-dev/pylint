class Animal:
    pass


class Fish:
    pass


class Cat(Animal):
    def __init__(self):
        super(Fish, self).__init__()  # [bad-super-call]
        super(Animal, self).__init__()
