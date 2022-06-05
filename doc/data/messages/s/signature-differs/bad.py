import abc


class Animal:
    @abc.abstractmethod
    def run(self, distance=0):
        pass


class Dog(Animal):
    def run(self, distance):  # [signature-differs]
        print(f"Ran {distance} km!")
        print("Fetched that stick, wuff !")
