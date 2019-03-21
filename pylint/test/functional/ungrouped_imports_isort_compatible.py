"""Checks import order rule with imports that isort could generate"""
# pylint: disable=unused-import
import astroid
import isort
from astroid import are_exclusive, decorators
from astroid.modutils import get_module_part, is_standard_module
