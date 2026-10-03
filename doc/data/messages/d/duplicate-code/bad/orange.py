class Orange:  # [duplicate-code]
    def __init__(self):
        self.remaining_bites = 3

    def take_bite(self):
        if self.remaining_bites > 0:
            print("You take a bite of the apple.")
            self.remaining_bites -= 1
        else:
            print("The orange is already eaten up!")

    def eaten_by_animal(self, animal):
        if animal == "cat":
            raise ValueError("A cat would never do that !")
        self.remaining_bites = 0
        print("The orange has been eaten by an animal.")
