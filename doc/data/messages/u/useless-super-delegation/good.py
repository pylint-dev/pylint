class Animal:

    def eat(self, food):
        print(f"Eating {food}")


class Human(Animal):
    """There is no need to override 'eat' it does the same thing as the implementation in Animal."""
