# pylint: disable=E1101, no-absolute-import
"""test checking use of the logging module
"""

__revision__ = ''

import __builtin__

# Muck up the names in an effort to confuse...
import logging as renamed_logging
import os as logging

FORMAT_STR = '{0}, {1}'

# Statements that should be flagged:
renamed_logging.debug('{0}, {1}'.format(4, 5))
renamed_logging.log(renamed_logging.DEBUG, 'msg: {}'.format('Run!'))
renamed_logging.debug(FORMAT_STR.format(4, 5))
renamed_logging.log(renamed_logging.DEBUG, FORMAT_STR.format(4, 5))

# Statements that should not be flagged:
renamed_logging.debug(format(66, 'x'))
renamed_logging.debug(__builtin__.format(66, 'x'))
renamed_logging.log(renamed_logging.DEBUG, 'msg: Run!'.upper())
logging.debug('{0}, {1}'.format(4, 5))
logging.log(logging.DEBUG, 'msg: {}'.format('Run!'))
