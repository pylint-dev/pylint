# pylint: disable=missing-docstring, consider-using-f-string

SEE = "see 👀"
SEA = "sea 🌊"

# +1: [duplicate-string-formatting-argument,duplicate-string-formatting-argument]
CONST = """
A sailor went to {}, {}, {}
To {} what he could {}, {}, {}
But all that he could {}, {}, {}
Was the bottom of the deep blue {}, {}, {}!
""".format(
    SEA,
    SEA,
    SEA,
    SEE,
    SEE,
    SEE,
    SEE,
    SEE,
    SEE,
    SEE,
    SEA,
    SEA,
    SEA,
)
