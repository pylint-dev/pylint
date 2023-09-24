# pylint: disable=missing-docstring

if (a := 2):
    pass

(b := 1)  # [named-expr-without-context]
