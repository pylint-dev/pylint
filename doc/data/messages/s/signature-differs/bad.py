import abc


class Animal:
    @abc.abstractmethod
    def run(self, distance=None):
        pass


class Dog(Animal):
    def run(self, distance):  # [signature-differs]
        print(f"Ran {distance} km!")
