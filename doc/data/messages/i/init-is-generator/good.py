class Fruit:
    def __init__(self, worms):
        self.__worms = worms

    def worms(self):
        yield from self.__worms


apple = Fruit(["Fahad", "Anisha", "Tabatha"])
for worm in apple.worms():
    pass
