# pylint: disable=missing-docstring, invalid-name, use-list-literal, use-tuple-literal
# https://github.com/PyCQA/pylint/issues/3165

list([])
tuple([])

list([0 for y in list(range(10))]) # [consider-using-generator]
tuple([0 for y in list(range(10))]) # [consider-using-generator]

list(0 for y in list(range(10)))
tuple(0 for y in list(range(10)))
