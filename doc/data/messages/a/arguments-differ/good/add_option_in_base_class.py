"""
Here we assume that drink and cocktail are the same thing and should actually
inherit from each over. We also assume that 'Drink' are 'Cocktail' without
alcohol (we added the alcohol option in the base class).

This permit to not have to modify the cocktails calls downstream but the case where
an alcohol is mixed in a soft drink will need to be handled.
"""


class Drink:
    def mix(self, fluid_one, fluid_two, alcoholic_fluid=None):
        # if alcoholic_fluid is not None:
        #     raise Exception(f"This soft drink has {alcoholic_fluid} in it !")
        return fluid_one + fluid_two


class Cocktail(Drink):
    def mix(self, fluid_one, fluid_two, alcoholic_fluid):
        return fluid_one + fluid_two + alcoholic_fluid
