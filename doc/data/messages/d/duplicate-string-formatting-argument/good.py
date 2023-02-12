# pylint: disable=missing-docstring, consider-using-f-string

SEE = "see 👀"
SEA = "sea 🌊"

# +1: [duplicate-string-formatting-argument,duplicate-string-formatting-argument]
CONST = """
A sailor went to {sea}, {sea}, {sea}
To {see} what he could {see}, {see}, {see}
But all that he could {see}, {see}, {see}
Was the bottom of the deep blue {sea}, {sea}, {sea}!
""".format(
    sea=SEA, see=SEE
)
