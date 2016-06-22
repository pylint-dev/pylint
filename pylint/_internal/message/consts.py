# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

import six


MSG_TYPES = {
    'I' : 'info',
    'C' : 'convention',
    'R' : 'refactor',
    'W' : 'warning',
    'E' : 'error',
    'F' : 'fatal'
    }
MSG_TYPES_LONG = {v: k for k, v in six.iteritems(MSG_TYPES)}

MSG_STATE_SCOPE_CONFIG = 0
MSG_STATE_SCOPE_MODULE = 1
MSG_STATE_CONFIDENCE = 2


class WarningScope(object):
    LINE = 'line-based-msg'
    NODE = 'node-based-msg'
