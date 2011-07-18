# pylint: disable=E1101
"""Test checking of log format strings
"""

__revision__ = ''

import logging

def pprint():
    """Test string format in logging statements.
    """
    # These should all emit lint errors:
    logging.info(0, '') # 1205
    logging.info('', '') # 1205
    logging.info('%s%', '') # 1201
    logging.info('%s%s', '') # 1206
    logging.info('%s%a', '', '') # 1200
    logging.info('%s%s', '', '', '') # 1205

    # These should be okay:
    logging.info(1)
    logging.info(True)
    logging.info('')
    logging.info('%s%')
    logging.info('%s', '')
    logging.info('%s%%', '')
    logging.info('%s%s', '', '')
