class Animal:
    def run(self, distance=0):
        print(f"Ran {distance} km!")


class Dog(Animal):
    def run(self, distance):  # [signature-differs]
        super(Animal, self).run(distance)
        print("Fetched that stick, wuff !")
