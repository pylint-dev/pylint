from fruit import Fruit


class Orange(Fruit):
    def eaten_by_animal(self, animal):
        if animal == "cat":
            raise ValueError("A cat would never do that !")
        super().eaten_by_animal(animal)
