def print_color(fruit):  # [consider-narrowing-parameter]
    print(fruit.color)


class Apple:
    color = "red"


print_color(Apple())
