class Animal:
    beaver_tailed: bool
    can_swim: bool
    has_beak: bool
    has_fur: bool
    has_vertebrae: bool
    lays_egg: bool
    protected_specie: bool
    venomous: bool


class Invertebrate(Animal):
    has_vertebrae = False


class Vertebrate(Animal):
    has_vertebrae = True


class Mammal(Vertebrate):
    has_beak = False
    has_fur = True
    lays_egg = False
    venomous = False


class Playtypus(Mammal):
    beaver_tailed = True
    can_swim = True
    has_beak = True
    lays_egg = True
    protected_specie = True
    venomous = True
