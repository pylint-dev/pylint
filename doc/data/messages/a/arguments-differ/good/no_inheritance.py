"""
Here we assume that 'Drink' and 'Cocktail' are different things and should
not be treated together like if they were the same thing.

This will force some downstream changes and force the API user to make a
conscious decision about the alcoholic content of its drink when using the
API. For example, it's impossible to create a mojito with beer without
explicitly wanting to, or to add an alcohol to a soft-drink.
"""


class Drink:
    def mix(self, fluid_one, fluid_two):
        return fluid_one + fluid_two


class Cocktail:
    def mix(self, fluid_one, fluid_two, alcoholic_fluid):
        return fluid_one + fluid_two + alcoholic_fluid
