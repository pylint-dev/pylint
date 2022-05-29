FLYING_THINGS = ["bird", "plane", "superman", "this example"]


def is_flying_animal(an_object):
    if isinstance(an_object, Animal) and an_object in FLYING_THINGS:  # [simplifiable-if-statement]
        is_flying = True
    else:
        is_flying = False
    return is_flying
