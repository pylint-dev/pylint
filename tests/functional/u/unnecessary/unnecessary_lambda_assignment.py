"""Test assignment of lambda expressions to a variable."""
# pylint: disable=unbalanced-tuple-unpacking, undefined-variable, line-too-long

a = lambda x: x  # [unnecessary-lambda-assignment]
a = (
    lambda x: x  # [unnecessary-lambda-assignment]
)
a, b = lambda x: x, lambda y: y  # [unnecessary-lambda-assignment,unnecessary-lambda-assignment]
a, b = (
    lambda x: x,  # [unnecessary-lambda-assignment]
    lambda y: y,  # [unnecessary-lambda-assignment]
)
a, b = 1, lambda y: y  # [unnecessary-lambda-assignment]
a, b = (
    1,
    lambda y: y  # [unnecessary-lambda-assignment]
)

# Interaction with W0632 (unbalanced-tuple-unpacking)
a, b = lambda x: x, lambda y: y, lambda z: z  # [unnecessary-lambda-assignment,unnecessary-lambda-assignment]
a, b = (
    lambda x: x,  # [unnecessary-lambda-assignment]
    lambda y: y,  # [unnecessary-lambda-assignment]
    lambda z: z,  # This isn't assigned so don't flag.
)
a, b, c = lambda x: x, lambda y: y  # [unnecessary-lambda-assignment,unnecessary-lambda-assignment]

# Only flag lambdas directly assigned to variables.
d["key"] = lambda x: x
squares = list(map(lambda x: x**2, range(10)))

DICT = {1: lambda x: x, 2: lambda x: x + 1}
for key, value in DICT.items():
    print(value(key))
