from typing import Any, TYPE_CHECKING

from mod_a import Int

if TYPE_CHECKING:
    from mod_a import List

def list_int(x: Any) -> List[Int]:
    return [x] if isinstance(x, Int) else []
