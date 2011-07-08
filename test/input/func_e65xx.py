# pylint: disable=E1101
"""Test checking of log format strings
"""

__revision__ = ''

import logging

def pprint():
    """Test string format in logging statements.
    """
    # These should all emit lint errors:
    logging.info(0, '') # 6505
    logging.info('', '') # 6505
    logging.info('%s%', '') # 6501
    logging.info('%s%s', '') # 6506
    logging.info('%s%a', '', '') # 6500
    logging.info('%s%s', '', '', '') # 6505

    # These should be okay:
    logging.info(1)
    logging.info(True)
    logging.info('')
    logging.info('%s%')
    logging.info('%s', '')
    logging.info('%s%%', '')
    logging.info('%s%s', '', '')
