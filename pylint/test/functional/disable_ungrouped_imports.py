"""Checks that disabling 'ungrouped-imports' on an import prevents subsequent
imports from being considered ungrouped in respect to it."""
# pylint: disable=unused-import,relative-import,wrong-import-position,wrong-import-order,using-constant-test
# pylint: disable=import-error
import os
import logging.config  # pylint: disable=ungrouped-imports
import os.path
import logging
from os.path import join  # [ungrouped-imports]
import logging.handlers  # [ungrouped-imports]
