class Fruit:
    FRUITS = ["apple", "orange"]

    def __contains__(self, name):
        return name in self.FRUITS


apple = "apple" in Fruit()
