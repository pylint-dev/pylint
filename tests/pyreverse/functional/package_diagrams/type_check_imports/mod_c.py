from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mod_a import Int

def some_int() -> Int:
    return 5
