import abc


class Animal:
    @abc.abstractmethod
    def run(self, distance=0):
        pass


class Dog(Animal):
    def run(self, distance=0):
        print(f"Ran {distance} km!")
