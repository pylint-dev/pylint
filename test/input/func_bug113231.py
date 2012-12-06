# pylint: disable=E1101
# pylint: disable=C0103
# pylint: disable=R0903
"""test bugfix for #113231 in logging checker
"""

__revision__ = ''

# Muck up the names in an effort to confuse...
import logging as renamed_logging

class Logger(object):
    """Fake logger"""
    pass

logger = renamed_logging.getLogger(__name__)
fake_logger = Logger()

# Statements that should be flagged:
renamed_logging.warn('%s, %s' % (4, 5))
logger.warn('%s' % 5)

# Statements that should not be flagged:
fake_logger.warn('%s' % 5)
