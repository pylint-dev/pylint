def print_color(color):
    print("This fruit is", color)
    print("I like", color)


class Apple:
    color = "red"


print_color(Apple().color)
