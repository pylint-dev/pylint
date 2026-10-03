from typing import final


class Animal:
    @final
    def can_breathe(self):
        return True


class Cat(Animal):
    def can_breathe(self):  # [overridden-final-method]
        pass
