class Animal:

    def eat(self, food):
        print(f"Eating {food}")


class Human(Animal):

    def eat(self, food):
        super(Human, self).eat()  # [useless-super-delegation]
