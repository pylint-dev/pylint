"""Test assignment of lambda expressions to a variable."""
# pylint: disable=unbalanced-tuple-unpacking,undefined-variable,line-too-long
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
# Example below is currently commented out due to
# https://github.com/PyCQA/pylint/issues/5998
# N.B. should raise 'unnecessary-lambda-assignment'
# I've just removed the inline comment for now as
# it's confusing the tester whilst commented out!
# a, b, c = lambda x: x, lambda y: y

# Only flag lambdas directly assigned to variables.
d["key"] = lambda x: x
squares = list(map(lambda x: x**2, range(10)))
