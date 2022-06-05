class Fruit:  # [single-string-used-for-slots]
    __slots__ = "price"

    def __init__(self, price):
        self.price = price
