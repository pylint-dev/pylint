class Worm:
    def __swallow(self):
        pass

    def eat(self):
        return self.__swallow()


jim = Worm()
jim.eat()
