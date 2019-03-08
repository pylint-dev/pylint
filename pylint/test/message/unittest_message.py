# -*- coding: utf-8 -*-

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

import io

import astroid

from pylint.message import MessagesStore, MessageDefinition
from pylint.checkers.utils import check_messages, get_node_last_lineno
from pylint.exceptions import InvalidMessageError
import pytest
