# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
import sys
from typing import NamedTuple, Optional, Tuple, Union

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


class Argument(NamedTuple):
    """Data about a argument to be parsed by argparse (or optparse until deprecation)
    Follows structure of the parameters for argparse.ArgumentParser.add_argument
    See https://docs.python.org/3/library/argparse.html#the-add-argument-method"""

    name: Tuple[str, ...]
    """Tuple of names or flags (i.e., -f or --foo)"""

    action: str
    """Action to do after"""

    nargs: Optional[int]
    """The number of command line arguments to capture"""

    const: Optional[str]
    """The const to store with certain types of actions"""

    default: Union[str, int, bool, None]
    """Default value"""

    argument_type: str
    """Name of validator"""

    help_string: str
    """Help message"""

    metavar: str
    """Metavar for help message"""


class StoreArgument(Argument):
    """Used to store a passed argument or default value"""

    def __new__(
        cls,
        name: Tuple[str, ...],
        action: Literal["store"],
        nargs: Literal[1],
        const: None,
        default: Union[str, int, bool, None],
        argument_type: Literal["yn"],
        help_string: str,
        metavar: Literal["<y_or_n>"],
    ) -> "StoreArgument":
        return Argument.__new__(
            cls,
            name,
            action,
            nargs,
            const,
            default,
            argument_type,
            help_string,
            metavar,
        )
