class FruitBasket:
    def __init__(self, fruits):
        self.fruits = ["Apple", "Banana", "Orange"]

    def __len__(self):  # [invalid-length-returned]
        return -len(self.fruits)
