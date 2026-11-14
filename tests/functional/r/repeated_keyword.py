"""Check that a keyword is not repeated in a function call

This is somehow related to redundant-keyword, but it's not the same.
"""

# pylint: disable=missing-docstring, invalid-name

def test(a, b):
    return a, b

test(1, 24)
test(1, b=24, **{})
test(1, b=24, **{'b': 24}) # [repeated-keyword]

# Built-in functions have no argument information, but a repeated keyword
# is still an error at call time (#6856).
print("Hello", sep=" ", end="!", **{"end": "?"})  # [repeated-keyword]
print("Hello", **{"sep": " ", "end": "!"}, **{"end": "?"})  # [repeated-keyword]
with open("file", "r", encoding="utf8", **{"encoding": "ascii"}) as f:  # [repeated-keyword]
    f.read()
print("Hello", sep=" ", **{"end": "!"})
print(**{"end": "!", "end": "?"})  # [duplicate-key]
