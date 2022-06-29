FLYING_THINGS = ["bird", "plane", "superman", "this example"]


def is_flying_thing(an_object):
    return True if an_object in FLYING_THINGS else False  # [simplifiable-if-expression]


def is_not_flying_thing(an_object):
    return False if an_object in FLYING_THINGS else True  # [simplifiable-if-expression]
