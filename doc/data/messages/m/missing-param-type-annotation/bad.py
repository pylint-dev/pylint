def greet(name) -> str:  # [missing-param-type-annotation]
    return f"Hello, {name}!"


def add(x, y) -> int:  # [missing-param-type-annotation, missing-param-type-annotation]
    return x + y


def process(  # [missing-param-type-annotation, missing-param-type-annotation]
    *args, **kwargs
) -> dict:
    return combine(args, kwargs)
