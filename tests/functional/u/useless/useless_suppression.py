"""Tests for useless suppressions"""
# pylint: enable=useless-suppression, line-too-long
# pylint: disable=unused-import, wrong-import-order

# False positive for wrong-import-order
# Reported in https://github.com/PyCQA/pylint/issues/2366
from pylint import run_pylint
import astroid

# False-positive for 'line-too-long'
# Reported in https://github.com/PyCQA/pylint/issues/4212
VAR = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" # pylint: disable=line-too-long
