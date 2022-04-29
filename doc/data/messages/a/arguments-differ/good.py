class Drink:
    def mix(self, fluid_one, fluid_two):
        return fluid_one + fluid_two


class Cocktail(Drink):
    def mix(self, fluid_one, fluid_two, alcoholic_fluid_one="Beer"):
        return fluid_one + fluid_two + alcoholic_fluid_one


class Car:
    tank = 0

    def fill_tank(self, gas):
        self.tank += gas


class Airplane:
    tank = 0
    kerosine_tank = 0

    def fill_tank(self, gas, kerosine):
        self.tank += gas
        self.kerosine_tank += kerosine
