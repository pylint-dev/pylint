fruit: str = "apple"


def function_returning_a_fruit() -> str:
    return "orange"


if fruit == function_returning_a_fruit():
    print("apple == orange")
