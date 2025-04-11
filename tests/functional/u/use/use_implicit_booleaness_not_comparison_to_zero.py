# pylint: disable=literal-comparison,missing-docstring, singleton-comparison

X = 123
Y = len('test')

if X is 0:  # [use-implicit-booleaness-not-comparison-to-zero]
    pass

if X is False:
    pass

if Y is not 0:  # [use-implicit-booleaness-not-comparison-to-zero]
    pass

if Y is not False:
    pass

if X == 0:  # [use-implicit-booleaness-not-comparison-to-zero]
    pass

if X == False:
    pass

if 0 == Y:  # [use-implicit-booleaness-not-comparison-to-zero]
    pass

if Y != 0:  # [use-implicit-booleaness-not-comparison-to-zero]
    pass

if 0 != X:  # [use-implicit-booleaness-not-comparison-to-zero]
    pass

if Y != False:
    pass

if X > 0:
    pass

if X < 0:
    pass

if 0 < X:
    pass

if 0 > X:
    pass

if X == Y == 0:
    pass

if 0 == X == Y:
    pass

if X == Y == X == Y == 0:
    pass


def test_in_boolean_context():
    """Cases where a comparison like `x != 0` is used in a boolean context.

    It is safe and idiomatic to simplify `x != 0` to just `x`.
    """
    # pylint: disable=pointless-statement,superfluous-parens,unnecessary-negation

    # Control flow
    if X != 0:  # [use-implicit-booleaness-not-comparison-to-zero]
        pass
    while X != 0:  # [use-implicit-booleaness-not-comparison-to-zero]
        pass
    assert X != 0  # [use-implicit-booleaness-not-comparison-to-zero]

    # Ternary
    _ = 1 if X != 0 else 2  # [use-implicit-booleaness-not-comparison-to-zero]

    # Not
    if not (X != 0):  # [use-implicit-booleaness-not-comparison-to-zero]
        pass

    # Comprehension filters
    [x for x in [] if X != 0]  # [use-implicit-booleaness-not-comparison-to-zero]
    {x for x in [] if X != 0}  # [use-implicit-booleaness-not-comparison-to-zero]
    (x for x in [] if X != 0)  # [use-implicit-booleaness-not-comparison-to-zero]

    # all() / any() with generator expressions
    all(X != 0 for _ in range(1))  # [use-implicit-booleaness-not-comparison-to-zero]
    any(X != 0 for _ in range(1))  # [use-implicit-booleaness-not-comparison-to-zero]

    # filter() with lambda
    filter(lambda: X != 0, [])  # [use-implicit-booleaness-not-comparison-to-zero]

    # boolean cast
    bool(X != 0)  # [use-implicit-booleaness-not-comparison-to-zero]

    # Logical operators nested in boolean contexts
    if X != 0 and input():  # [use-implicit-booleaness-not-comparison-to-zero]
        pass
    while input() or X != 0:  # [use-implicit-booleaness-not-comparison-to-zero]
        pass
    if (X != 0 or input()) and input():  # [use-implicit-booleaness-not-comparison-to-zero]
        pass


def test_not_in_boolean_context():
    """Cases where a comparison like `x != 0` is used in a non-boolean context.

    These comparisons cannot be safely replaced with just `x`, and should be explicitly
    cast using `bool(x)`.
    """
    # pylint: disable=pointless-statement
    _ = X != 0  # [use-implicit-booleaness-not-comparison-to-zero]

    _ = X != 0 or input()  # [use-implicit-booleaness-not-comparison-to-zero]

    print(X != 0)  # [use-implicit-booleaness-not-comparison-to-zero]

    [X != 0 for _ in []]  # [use-implicit-booleaness-not-comparison-to-zero]

    lambda: X != 0  # [use-implicit-booleaness-not-comparison-to-zero]

    filter(lambda x: x, [X != 0])  # [use-implicit-booleaness-not-comparison-to-zero]

    return X != 0  # [use-implicit-booleaness-not-comparison-to-zero]
