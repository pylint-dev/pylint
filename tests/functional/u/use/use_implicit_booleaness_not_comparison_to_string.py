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
