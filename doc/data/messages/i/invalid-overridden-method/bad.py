class Fruit:
    async def bore(self):
        pass

class Worm(Fruit):
    def bore(self):  # [invalid-overridden-method]
        pass
