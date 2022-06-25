class Animal:
    def __init__(self):
        self.is_multicellular = True


class Vertebrate(Animal):
    def __init__(self):
        super().__init__()
        self.has_vertebrae = True


class Cat(Vertebrate):
    def __init__(self):
        super().__init__()
        self.is_adorable = True
