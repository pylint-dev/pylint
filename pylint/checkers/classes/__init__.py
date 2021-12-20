# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

from typing import TYPE_CHECKING

from pylint.checkers.classes.class_checker import ClassChecker
from pylint.checkers.classes.special_methods_checker import SpecialMethodsChecker

if TYPE_CHECKING:
    from pylint.lint import PyLinter


def register(linter: "PyLinter") -> None:
    """This required method auto registers the checker during initialization.

    :param linter: The linter to register the checker to.
    """
    linter.register_checker(ClassChecker(linter))
    linter.register_checker(SpecialMethodsChecker(linter))
