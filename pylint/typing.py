# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""A collection of typing utilities."""
import sys
from typing import TYPE_CHECKING, Dict, List, NamedTuple, Union

if TYPE_CHECKING:
    from typing import Counter  # typing.Counter added in Python 3.6.1

if sys.version_info >= (3, 8):
    from typing import Literal, TypedDict
else:
    from typing_extensions import Literal, TypedDict


class FileItem(NamedTuple):
    """Represents data about a file handled by pylint

    Each file item has:
    - name: full name of the module
    - filepath: path of the file
    - modname: module name
    """

    name: str
    filepath: str
    modpath: str


class ModuleDescriptionDict(TypedDict):
    """Represents data about a checked module"""

    path: str
    name: str
    isarg: bool
    basepath: str
    basename: str


class ErrorDescriptionDict(TypedDict):
    """Represents data about errors collected during checking of a module"""

    key: Literal["fatal"]
    mod: str
    ex: Union[ImportError, SyntaxError]


# The base type of the "stats" attribute of a checker
CheckerStats = Dict[
    str, Union[int, "Counter[str]", List, Dict[str, Union[int, str, Dict[str, int]]]]
]
