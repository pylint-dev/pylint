# pylint: disable=missing-docstring, invalid-name
# https://github.com/PyCQA/pylint/issues/3165

any([])
all([])

any([0 for x in list(range(10))]) # [use-a-generator]
all([0 for y in list(range(10))]) # [use-a-generator]

any(0 for x in list(range(10)))
all(0 for y in list(range(10)))
