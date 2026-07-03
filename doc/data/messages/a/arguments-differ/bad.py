class Drink:
    def mix(self, fluid_one, fluid_two):
        return fluid_one + fluid_two


class Cocktail(Drink):
    def mix(self, fluid_one, fluid_two, alcoholic_fluid):  # [arguments-differ]
        return fluid_one + fluid_two + alcoholic_fluid
