class Animal:
    def eat(self, food):
        print(f"Eating {food}")


class Human(Animal):
    """There is no need to override 'eat' it has the same signature as the implementation in Animal."""
