# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

import collections
from typing import TYPE_CHECKING, Dict, List, Union

from pylint.typing import CheckerStats

if TYPE_CHECKING:
    from typing import Counter  # typing.Counter added in Python 3.6.1


def merge_stats(stats: List[CheckerStats]):
    """Used to merge two stats objects into a new one when pylint is run in parallel mode"""
    merged: CheckerStats = {}
    by_msg: "Counter[str]" = collections.Counter()
    for stat in stats:
        message_stats: Union["Counter[str]", Dict] = stat.pop("by_msg", {})  # type: ignore
        by_msg.update(message_stats)

        for key, item in stat.items():
            if key not in merged:
                merged[key] = item
            elif isinstance(item, dict):
                merged[key].update(item)  # type: ignore
            else:
                merged[key] = merged[key] + item  # type: ignore

    merged["by_msg"] = by_msg
    return merged
