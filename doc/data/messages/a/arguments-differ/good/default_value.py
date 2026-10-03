"""
Here we assume that drink and cocktail are the same thing and should actually
inherit from each over. We also assume that any Cocktail can be treated like
a Drink (if you add beer to it).

This permit to not have to modify the calls downstream and causes the least
amount of disturbance at the cost of making cocktails beer-based implicitly.
"""


class Drink:
    def mix(self, fluid_one, fluid_two):
        return fluid_one + fluid_two


class Cocktail(Drink):
    def mix(self, fluid_one, fluid_two, alcoholic_fluid="Beer"):
        return fluid_one + fluid_two + alcoholic_fluid
