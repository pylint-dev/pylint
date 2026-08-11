def _print_color(color):
    print("This fruit is", color)
    print("I like", color)


class Apple:
    color = "red"


_print_color(Apple().color)
