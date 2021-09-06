# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""A collection of typing utilities
"""

from typing import Counter, Dict, List, Union

# The base type of the "stats" attribute of a checker
CheckerStatistics = Dict[
    str, Union[int, Counter[str], List, Dict[str, Union[int, str, Dict[str, int]]]]
]
