# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""A collection of typing utilities."""
from typing import TYPE_CHECKING, Dict, List, Union

if TYPE_CHECKING:
    from typing import Counter  # typing.Counter added in Python 3.6.1


# The base type of the "stats" attribute of a checker
CheckerStats = Dict[
    str, Union[int, "Counter[str]", List, Dict[str, Union[int, str, Dict[str, int]]]]
]
