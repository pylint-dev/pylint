from typing import final


@final  # [using-final-decorator-in-unsupported-version]
class Playtypus(Animal):
    @final  # [using-final-decorator-in-unsupported-version]
    def lay_egg(self): ...
