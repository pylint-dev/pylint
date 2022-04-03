fruit: str = "apple"


def function_returning_a_fruit() -> str:
    return "orange"


if fruit == function_returning_a_fruit:  # [comparison-with-callable]
    print("apple == <function function_returning_a_fruit at 0x7f343ff0a1f0>")
