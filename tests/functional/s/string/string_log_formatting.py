"""
Test checking of log format strings
"""

import logging


def pprint():
    """
    Test string format in logging statements.
    """

    # These should all emit lint errors:
    logging.info(0, '')  # [logging-too-many-args]
    logging.info('', '') # [logging-too-many-args]
    logging.info('%s%', '') # [logging-format-truncated]
    logging.info('%s%s', '') # [logging-too-few-args]
    logging.info('%s%y', '', '') # [logging-unsupported-format]
    logging.info('%s%s', '', '', '') # [logging-too-many-args]

    # These should be okay:
    logging.info(1)
    logging.info(True)
    logging.info('')
    logging.info('%s%')
    logging.info('%s', '')
    logging.info('%s%%', '')
    logging.info('%s%s', '', '')
