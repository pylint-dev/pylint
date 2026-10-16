# pylint: disable=missing-module-docstring

# Should not trigger undefined-variable (#10562)
item = (1, 2, 3)
for item in item:
    print(item)

# Should trigger undefined-variable
for iteree in iteree:  # [undefined-variable]
    print(iteree)
