# pylint: disable=missing-docstring

NAME = 42
OTHER_NAME = 24
OTHER_OTHER_NAME = 2

# +1: [duplicate-string-formatting-argument,duplicate-string-formatting-argument]
CONST = "some value {} some other value {} {} {} {} {}".format(
    NAME,
    NAME,
    OTHER_NAME,
    OTHER_NAME,
    OTHER_NAME,
    OTHER_OTHER_NAME,
)
