def greet(name):  # [missing-param-type-annotation]
    return f"Hello, {name}!"


def add(x, y) -> int:  # [missing-param-type-annotation, missing-param-type-annotation]
    return x + y


def process(*args, **kwargs):  # [missing-param-type-annotation, missing-param-type-annotation]
    return combine(args, kwargs)
