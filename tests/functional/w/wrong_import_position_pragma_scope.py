"""Test that wrong-import-position pragma suppression is correctly scoped."""
# pylint: disable=unused-import,invalid-name

import logging
import sys

# This pragma should not affect subsequent import statements
logger = logging.getLogger()  # pylint: disable=wrong-import-position
logging.basicConfig(level='DEBUG')

logger.debug('importing modules...')
import os  # [wrong-import-position]
import pathlib  # [wrong-import-position]
import random  # [wrong-import-position]
logger.debug('done importing')

# Test that pragma on import line works correctly (this import should not be flagged)
constant_var = "test"
import json  # pylint: disable=wrong-import-position

# Test that subsequent imports are not affected by the pragma above
import csv  # [wrong-import-position]
import re  # [wrong-import-position]
