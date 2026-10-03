# Only declared, the implementation is somewhere else (a C extension, or
# another module): https://github.com/pylint-dev/pylint/issues/9354

from typing import Iterator


class Declared:
    def __iter__(self) -> Iterator[int]: ...


def declared_tuple() -> tuple[int, int, int]:
    ...

def declared_int() -> int:
    ...

# The annotation names the class of the returned value.
def declared_class() -> Declared:
    ...

# A forward reference the stub leaves unresolved: the annotation is a plain
# string, so there is nothing to infer from it.
def declared_unresolved() -> "NeverDefinedAnywhere":
    ...

# A stub that declares no return type at all.
def declared_without_annotation():
    ...

# A stub that declares ``None`` explicitly.
def declared_none() -> None:
    ...
