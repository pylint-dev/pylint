class Animal:

    def eat(self, food):
        print(f"Eating {food}")


class Human(Animal):

    def eat(self, food):  # [useless-super-delegation]
        super(Human, self).eat(food)
