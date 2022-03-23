# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Permits separating multiple checks with the same checker name into classes/file."""

from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


class _BasicChecker(BaseChecker):
    __implements__ = IAstroidChecker
    name = "basic"
