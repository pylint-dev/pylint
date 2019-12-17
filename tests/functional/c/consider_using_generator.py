# pylint: disable=missing-docstring, invalid-name
# https://github.com/PyCQA/pylint/issues/3165

any([])
all([])

any([0 for x in list(range(10))]) # [consider-using-generator]
all([0 for y in list(range(10))]) # [consider-using-generator]

any(0 for x in list(range(10)))
all(0 for y in list(range(10)))

any(list(range(10)))
all(list(range(10)))
