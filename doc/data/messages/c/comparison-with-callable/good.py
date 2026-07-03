def function_returning_a_fruit() -> str:
    return "orange"


def is_an_orange(fruit: str = "apple"):
    # apple == orange
    return fruit == function_returning_a_fruit()
