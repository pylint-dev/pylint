class Fruit:
    async def bore(self, insect):
        insect.eat(self)


class Apple(Fruit):
    async def bore(self, insect):
        insect.eat(self)
