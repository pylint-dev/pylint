"""
Regression test for https://github.com/PyCQA/pylint/issues/3979
"""

import os
from typing import TYPE_CHECKING, Any, Union

if TYPE_CHECKING:
    BasePathLike = os.PathLike[Any]  # <-- that is where pylint identifies E1136
else:
    BasePathLike = os.PathLike

foo : Union[str, BasePathLike] = "bar"
