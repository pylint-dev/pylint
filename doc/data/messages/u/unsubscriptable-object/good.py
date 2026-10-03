class Fruit:
    def __init__(self):
        self.colors = ["red", "orange", "yellow"]

    def __getitem__(self, idx):
        return self.colors[idx]


Fruit()[1]
