from typing import TYPE_CHECKING

from mod_a import Int

if TYPE_CHECKING:
    from mod_a import List
    from typing import Any

def list_int(x: Any) -> List[Int]:
    return [x] if isinstance(x, Int) else []
