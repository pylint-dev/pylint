# Copyright (c) 2003-2016 LOGILAB S.A. (Paris, FRANCE).
# http://www.logilab.fr/ -- mailto:contact@logilab.fr
# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

import warnings

from pylint.extensions import docparams


def register(linter):
    """Required method to auto register this checker.

    :param linter: Main interface object for Pylint plugins
    :type linter: Pylint object
    """
    warnings.warn("This plugin is deprecated, use pylint.extensions.docparams instead.",
                  DeprecationWarning)
    linter.register_checker(docparams.DocstringParameterChecker(linter))
