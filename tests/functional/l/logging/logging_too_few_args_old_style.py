"""Tests for logging-too-few-args old style"""

import logging

logging.error("%s, %s", 1)  # [logging-too-few-args]
logging.debug("Sisyphus table %s: sleep")  # [logging-too-few-args]
