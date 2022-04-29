class Drink:
    def mix(self, fluid_one, fluid_two):
        return fluid_one + fluid_two


class Cocktail(Drink):
    def mix(self, fluid_one, fluid_two, alcoholic_fluid_one):  # [arguments-differ]
        return fluid_one + fluid_two + alcoholic_fluid_one


class Car:
    tank = 0

    def fill_tank(self, gas):
        self.tank += gas


class Airplane(Car):
    kerosene_tank = 0

    def fill_tank(self, gas, kerosene):  # [arguments-differ]
        self.tank += gas
        self.kerosene_tank += kerosene
