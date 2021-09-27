"""Test for useless suppression false positive for wrong-import-order
Reported in https://github.com/PyCQA/pylint/issues/2366"""
# pylint: enable=useless-suppression
# pylint: disable=unused-import, wrong-import-order
from pylint import run_pylint
import astroid
