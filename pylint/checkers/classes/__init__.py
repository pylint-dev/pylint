# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE


from pylint.checkers.classes.class_checker import ClassChecker
from pylint.checkers.classes.special_methods_checker import SpecialMethodsChecker


def register(linter):
    """required method to auto register this checker"""
    linter.register_checker(ClassChecker(linter))
    linter.register_checker(SpecialMethodsChecker(linter))
