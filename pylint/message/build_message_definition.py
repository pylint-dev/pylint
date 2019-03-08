# -*- coding: utf-8 -*-

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

import warnings

from pylint.interfaces import IRawChecker, ITokenChecker, implements
from pylint.message.message_definition import MessageDefinition
from pylint.utils.warning_scope import WarningScope


def build_message_def(checker, msgid, msg_tuple):
    if implements(checker, (IRawChecker, ITokenChecker)):
        default_scope = WarningScope.LINE
    else:
        default_scope = WarningScope.NODE
    options = {}
    if len(msg_tuple) > 3:
        (msg, symbol, descr, options) = msg_tuple
    elif len(msg_tuple) > 2:
        (msg, symbol, descr) = msg_tuple
    else:
        # messages should have a symbol, but for backward compatibility
        # they may not.
        (msg, descr) = msg_tuple
        warnings.warn(
            "[pylint 0.26] description of message %s doesn't include "
            "a symbolic name" % msgid,
            DeprecationWarning,
        )
        symbol = None
    options.setdefault("scope", default_scope)
    return MessageDefinition(checker, msgid, msg, descr, symbol, **options)
