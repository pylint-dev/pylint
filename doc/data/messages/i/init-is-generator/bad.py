class Fruit:
    def __init__(self, worms):  # [init-is-generator]
        yield from worms


apple = Fruit(["Fahad", "Anisha", "Tabatha"])
