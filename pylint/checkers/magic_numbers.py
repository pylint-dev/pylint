# -*- coding: utf-8 -*-
# Copyright (c) 2016 Lukasz Rogalski <rogalski.91@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Checker that looks for places where constant may be used instead of magic number."""
import errno
import re
import sys

import astroid

from pylint import checkers
from pylint import interfaces
from pylint.checkers import utils
from pylint.checkers.utils import check_messages

RE_FLAGS = {getattr(re, f): 're.' + f for f in dir(re)
            if f.isupper() and len(f) > 1 and not f.startswith("_")}
ERRNO_VALUES = errno.errorcode

EXC_MODULE = 'exceptions' if sys.version_info < (3, 0) else 'builtins'
OSERROR_QNAME = EXC_MODULE + ".OSError"


def is_oserror_errno(node):
    if not isinstance(node, astroid.Attribute) or not node.attrname == 'errno':
        return False
    inferred = utils.safe_infer(node.expr)
    return inferred is not None and inferred.qname() == OSERROR_QNAME


def is_const(node):
    return isinstance(node, astroid.Const)


def is_literal_of_consts(node):
    return (isinstance(node, (astroid.List, astroid.Set, astroid.Tuple)) and
            all(is_const(elt) for elt in node.elts))


def const_value_to_bitwise_flags(const_value, flags):
    bitwise_flags = set()
    for flag_value, qname in flags.items():
        if flag_value & const_value:
            bitwise_flags.add(qname)
    return sorted(bitwise_flags)


class MagicNumberChecker(checkers.BaseChecker):
    """MagicNumberChecker warns when literal is used
    instead of predefined constant."""
    __implements__ = (interfaces.IAstroidChecker,)

    # configuration section name
    name = 'magic_numbers'
    msgs = {
        'W2001': ('Avoid using magic numbers, use %s instead of %s',
                  'magic-number-used',
                  'Used when Pylint detects magic number usage when '
                  'predefined constants are known'),
    }

    priority = -1
    options = ()

    @check_messages('magic-number-used')
    def visit_call(self, node):
        func = utils.safe_infer(node.func)
        if not isinstance(func, astroid.FunctionDef):
            return
        qname = func.qname()
        if qname.startswith('re.'):
            self._visit_re_call(node, qname)

    def _visit_re_call(self, node, qname):
        if qname == 're.compile':
            self._check_re_calls(node, 1, 'flags')
        elif qname in {'re.search', 're.match', 're.findall', 're.finditer'}:
            self._check_re_calls(node, 2, 'flags')
        elif qname == 're.split':
            self._check_re_calls(node, 3, 'flags')
        elif qname in {'re.sub', 're.subn'}:
            self._check_re_calls(node, 4, 'flags')

    def _check_re_calls(self, node, flags_pos, flags_kw):
        try:
            call_flags = utils.get_argument_from_call(node, position=flags_pos, keyword=flags_kw)
        except utils.NoSuchArgumentError:
            return

        if is_const(call_flags):
            value = call_flags.value
        else:
            return

        bitwise_consts = ' | '.join(const_value_to_bitwise_flags(value, RE_FLAGS))
        self.add_message('magic-number-used', node=node,
                         args=(bitwise_consts, call_flags.as_string()))

    def visit_compare(self, node):
        if is_oserror_errno(node.left):
            self._check_oserror_errno_compare(node)

    def _check_oserror_errno_compare(self, node):
        for op, other in node.ops:
            if is_const(other):
                self._check_oserror_errno_const_comparison(node, other)
            elif op in {'in', 'not in'} and is_literal_of_consts(other):
                self._check_oserror_errno_membership(node, other)

    def _check_oserror_errno_membership(self, node, other):
        if any(elt.value in ERRNO_VALUES for elt in other.elts):
            elts = other.elts
            fixed_elts = [astroid.Name('errno.' + ERRNO_VALUES[elt.value])
                          if elt.value in ERRNO_VALUES else elt for elt in elts]
            fixed_node = type(other)()
            fixed_node.postinit(fixed_elts)
            self.add_message('magic-number-used', node=node,
                             args=(fixed_node.as_string(), other.as_string()))

    def _check_oserror_errno_const_comparison(self, node, other):
        value = other.value
        if value in ERRNO_VALUES:
            fixed_value = 'errno.' + ERRNO_VALUES[value]
            self.add_message('magic-number-used', node=node,
                             args=(fixed_value, str(value)))


def register(linter):
    """required method to auto register this checker """
    linter.register_checker(MagicNumberChecker(linter))
