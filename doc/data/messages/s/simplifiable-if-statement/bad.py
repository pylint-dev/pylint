FLYING_THINGS = ["bird", "plane", "superman", "this example"]


def is_flying_animal(an_object):
    if (  # [simplifiable-if-statement]
        isinstance(an_object, Animal) and an_object in FLYING_THINGS
    ):
        is_flying = True
    else:
        is_flying = False
    return is_flying
