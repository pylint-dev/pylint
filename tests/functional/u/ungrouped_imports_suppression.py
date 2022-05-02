"""Check ungrouped import and interaction with useless-suppression.

Previously disabling ungrouped-imports would always lead to useless-suppression.
"""
# pylint: enable=useless-suppression
# pylint: disable=unused-import, wrong-import-order

import logging.config
import os.path
from astroid import are_exclusive  # pylint: disable=ungrouped-imports # [useless-suppression]
import logging.handlers  # pylint: disable=ungrouped-imports # This should not raise useless-suppression
try:
    import os  # [ungrouped-imports]
except ImportError:
    pass
