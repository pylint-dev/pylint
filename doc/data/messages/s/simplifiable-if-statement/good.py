FLYING_THINGS = ["bird", "plane", "superman", "this example"]


def is_flying_animal(an_object):
    is_flying = isinstance(an_object, Animal) and an_object.name in FLYING_THINGS
    return is_flying
