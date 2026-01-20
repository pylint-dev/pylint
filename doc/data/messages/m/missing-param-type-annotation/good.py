def greet(name: str) -> str:
    return f"Hello, {name}!"


def add(x: int, y: int) -> int:
    return x + y


def process(*args: str, **kwargs: bool) -> dict:
    return combine(args, kwargs)


class Calculator:
    def compute(self, x: int, y: int) -> int:  # self doesn't need annotation
        return x + y
