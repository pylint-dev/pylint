class Animal:
    def run(self, distance=0):
        print(f"Ran {distance} km!")


class Dog(Animal):
    def run(self, distance=0):
        super(Animal, self).run(distance)
        print("Fetched that stick, wuff !")
