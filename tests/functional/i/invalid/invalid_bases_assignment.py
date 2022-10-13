# pylint: disable=missing-module-docstring, missing-class-docstring
# pylint: disable=too-few-public-methods


class Apple:
    pass


Apple.__bases__ = ()  # [invalid-bases-assignment]
Apple.__bases__ = "lala"  # [invalid-bases-assignment]
Apple.__bases__ = True  # [invalid-bases-assignment]
Apple.__bases__ = (1,)
Apple.__bases__ = ("red", "green")

bases = ("orange", "yellow")
Apple.__bases__ = bases  # [invalid-bases-assignment]
