# pylint: disable=literal-comparison,missing-docstring

X = ''
Y = 'test'

if X is '':  # [use-implicit-booleaness-not-comparison-to-string]
    pass

if Y is not "":  # [use-implicit-booleaness-not-comparison-to-string]
    pass

if X == "":  # [use-implicit-booleaness-not-comparison-to-string]
    pass

if Y != '':  # [use-implicit-booleaness-not-comparison-to-string]
    pass

if "" == Y:  # [use-implicit-booleaness-not-comparison-to-string]
    pass

if '' != X:  # [use-implicit-booleaness-not-comparison-to-string]
    pass

if X == Y == "":
    pass

if "" == X == Y:
    pass

if X == Y == X == Y == "":
    pass


def test_in_boolean_context():
    """Cases where a comparison like `x != ""` is used in a boolean context.

    It is safe and idiomatic to simplify `x != ""` to just `x`.
    """
    # pylint: disable=pointless-statement,superfluous-parens,unnecessary-negation

    # Control flow
    if X != "":  # [use-implicit-booleaness-not-comparison-to-string]
        pass
    while X != "":  # [use-implicit-booleaness-not-comparison-to-string]
        pass
    assert X != ""  # [use-implicit-booleaness-not-comparison-to-string]

    # Ternary
    _ = 1 if X != "" else 2  # [use-implicit-booleaness-not-comparison-to-string]

    # Not
    if not (X != ""):  # [use-implicit-booleaness-not-comparison-to-string]
        pass

    # Comprehension filters
    [x for x in [] if X != ""]  # [use-implicit-booleaness-not-comparison-to-string]
    {x for x in [] if X != ""}  # [use-implicit-booleaness-not-comparison-to-string]
    (x for x in [] if X != "")  # [use-implicit-booleaness-not-comparison-to-string]

    # all() / any() with generator expressions
    all(X != "" for _ in range(1))  # [use-implicit-booleaness-not-comparison-to-string]
    any(X != "" for _ in range(1))  # [use-implicit-booleaness-not-comparison-to-string]

    # filter() with lambda
    filter(lambda: X != "", [])  # [use-implicit-booleaness-not-comparison-to-string]

    # boolean cast
    bool(X != "")  # [use-implicit-booleaness-not-comparison-to-string]

    # Logical operators nested in boolean contexts
    if X != "" and input():  # [use-implicit-booleaness-not-comparison-to-string]
        pass
    while input() or X != "":  # [use-implicit-booleaness-not-comparison-to-string]
        pass
    if (X != "" or input()) and input():  # [use-implicit-booleaness-not-comparison-to-string]
        pass


def test_not_in_boolean_context():
    """Cases where a comparison like `x != ""` is used in a non-boolean context.

    These comparisons cannot be safely replaced with just `x`, and should be explicitly
    cast using `bool(x)`.
    """
    # pylint: disable=pointless-statement
    _ = X != ""  # [use-implicit-booleaness-not-comparison-to-string]

    _ = X != "" or input()  # [use-implicit-booleaness-not-comparison-to-string]

    print(X != "")  # [use-implicit-booleaness-not-comparison-to-string]

    [X != "" for _ in []]  # [use-implicit-booleaness-not-comparison-to-string]

    lambda: X != ""  # [use-implicit-booleaness-not-comparison-to-string]

    filter(lambda x: x, [X != ""])  # [use-implicit-booleaness-not-comparison-to-string]

    return X != ""  # [use-implicit-booleaness-not-comparison-to-string]
