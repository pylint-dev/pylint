class DefinitionOrder:
    zebra = 1
    aardvark: int = 2

    def __init__(self):
        self.yak = "yak"
        self.bison = 3

    @property
    def mongoose(self) -> str:
        return "mongoose"

    def walk(self):
        self.cat = 4

    def feed(self):
        pass
