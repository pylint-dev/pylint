# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""A collection of typing utilities."""
from typing import NamedTuple


# Represents data about a file handled by pylint
class FileItem(NamedTuple):
    name: str
    filepath: str
    modpath: str
