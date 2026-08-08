def _print_color(fruit):  # [consider-narrowing-parameter]
    print("This fruit is", fruit.color)
    print("I like", fruit.color)


class Apple:
    color = "red"


_print_color(Apple())
