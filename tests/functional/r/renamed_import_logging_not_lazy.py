# pylint: disable=missing-docstring, too-few-public-methods, no-member

from __future__ import absolute_import
# Muck up the names in an effort to confuse...
import logging as renamed_logging


class Logger:
    """Fake logger"""


logger = renamed_logging.getLogger(__name__)
fake_logger = Logger()

# Statements that should be flagged
renamed_logging.warning('%s, %s' % (4, 5))  # [logging-not-lazy]
logger.warning('%s' % 5)  # [logging-not-lazy]

# Statements that should not be flagged:
fake_logger.warn('%s' % 5)
