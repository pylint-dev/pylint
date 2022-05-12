# pylint: disable=missing-docstring, invalid-name
# https://github.com/PyCQA/pylint/issues/3165

any([])
all([])
sum([])
min([])
max([])

any([0 for x in list(range(10))]) # [use-a-generator]
all([0 for y in list(range(10))]) # [use-a-generator]
sum([x*x for x in range(10)]) # [use-a-generator])
min([x*x for x in range(10)]) # [use-a-generator])
max([x*x for x in range(10)]) # [use-a-generator])

any(0 for x in list(range(10)))
all(0 for y in list(range(10)))
sum(x*x for x in range(10))
min(x*x for x in range(10))
max(x*x for x in range(10))
