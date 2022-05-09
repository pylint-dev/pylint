"""Test assignment of lambda expressions to a variable."""
# Flag lambda expression assignments via named expressions as well.
if (c := lambda: 2) and c():  # [unnecessary-lambda-assignment]
    pass
