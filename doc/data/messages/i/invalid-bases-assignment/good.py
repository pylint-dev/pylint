class Apple:
    pass

Apple.__bases__ = ("green", "red", )  # [invalid-bases-assignment]
