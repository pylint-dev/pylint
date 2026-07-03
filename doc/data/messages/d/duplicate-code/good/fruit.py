class Fruit:
    def __init__(self):
        self.remaining_bites = 3

    def take_bite(self):
        if self.remaining_bites > 0:
            print(f"You take a bite of the {self.__class__.__name__.lower()}.")
            self.remaining_bites -= 1
        else:
            print(f"The {self.__class__.__name__.lower()} is already eaten up!")

    def eaten_by_animal(self, animal):
        self.remaining_bites = 0
        print(f"The {self.__class__.__name__.lower()} has been eaten by an animal.")
