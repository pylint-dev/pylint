# Only declared, the implementation is somewhere else (a C extension, or
# another module): https://github.com/pylint-dev/pylint/issues/9354

def declared_tuple() -> tuple[int, int, int]:
    ...

def declared_int() -> int:
    ...
