class Fruit:
    async def bore(self, insect):
        insect.eat(self)


class Apple(Fruit):
    def bore(self, insect):  # [invalid-overridden-method]
        insect.eat(self)
