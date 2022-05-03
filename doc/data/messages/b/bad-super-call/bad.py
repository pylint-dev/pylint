class Animal:
    pass


class Cat(Animal):
    def __init__(self):
        super(Animal, self).__init__()  # [bad-super-call]
