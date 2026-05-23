"""
Regression test for https://github.com/pylint-dev/pylint/issues/3979
"""

import os
from typing import TYPE_CHECKING, Any, Union

if TYPE_CHECKING:
    BasePathLike = os.PathLike[Any]  # <-- pylint used to emit E1136 here
else:
    BasePathLike = os.PathLike

FOO: Union[str, BasePathLike] = "bar"
