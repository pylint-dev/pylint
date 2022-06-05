import abc


class Animal:
    @abc.abstractmethod
    def run(self, distance=0):
        pass


class Dog(Animal):
    def run(self, distance=0):
        super(Animal, self).run(distance)
        print("Fetched that stick, wuff !")
