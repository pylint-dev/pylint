# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/LICENSE

from typing import Optional

__version__ = "3.0.0"
# For an official release, use 'alpha_version = False' and 'dev_version = None'
alpha_version: bool = True  # Release will be an alpha version if True (ex: '1.2.3a6')
dev_version: Optional[int] = 3

if dev_version is not None:
    if alpha_version:
        __version__ += f"a{dev_version}"
    else:
        __version__ += f".dev{dev_version}"
