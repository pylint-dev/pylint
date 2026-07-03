def function_returning_a_fruit() -> str:
    return "orange"


def is_an_orange(fruit: str = "apple"):
    # apple == <function function_returning_a_fruit at 0x7f343ff0a1f0>
    return fruit == function_returning_a_fruit  # [comparison-with-callable]
