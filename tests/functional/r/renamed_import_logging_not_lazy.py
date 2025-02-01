# pylint: disable=missing-docstring, too-few-public-methods, no-member, consider-using-f-string

from __future__ import absolute_import
# Muck up the names in an effort to confuse...
import logging as renamed_logging


class Logger:
    """Fake logger"""


LOGGER = renamed_logging.getLogger(__name__)
FAKE_LOGGER = Logger()

# Statements that should be flagged
renamed_logging.warning('%s, %s' % (4, 5))  # [logging-not-lazy]
LOGGER.warning('%s' % 5)  # [logging-not-lazy]

# Statements that should not be flagged:
FAKE_LOGGER.warn('%s' % 5)
