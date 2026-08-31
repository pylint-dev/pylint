from collections.abc import GenericAlias


class C:
    pass


x = C.a

for GenericAlias.a in _:
    pass
