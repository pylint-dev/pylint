# Copyright (c) 2014-2015 Bruno Daniel <bruno.daniel@blue-yonder.com>
# Copyright (c) 2015-2016, 2018, 2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2016 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2020 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2021 Marc Mueller <30130371+cdce8p@users.noreply.github.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

import warnings
from typing import TYPE_CHECKING

from pylint.extensions import docparams

if TYPE_CHECKING:
    from pylint.lint import PyLinter


def register(linter: "PyLinter") -> None:
    """This required method auto registers the checker during initialization.

    :param linter: The linter to register the checker to.
    """
    warnings.warn(
        "This plugin is deprecated, use pylint.extensions.docparams instead.",
        DeprecationWarning,
    )
    linter.register_checker(docparams.DocstringParameterChecker(linter))
