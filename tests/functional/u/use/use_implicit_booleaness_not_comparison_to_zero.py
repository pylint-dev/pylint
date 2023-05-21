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
